
from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    """Modelo que representa un Área de Conocimiento."""
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    """Modelo 1 a 1 con User para manejar roles y tracking de actividad."""
    ROLES = (
        ('ESTUDIANTE', 'Estudiante'),
        ('COORDINADOR', 'Coordinador'),
        ('ADMIN', 'Administrador Global'),
    )
    """
    RR - Relación 1:1: ¿Qué es? Es un vínculo exclusivo. Un Usuario nativo de Django solo puede tener un único PerfilUsuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    ultima_actividad = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Curso(models.Model):
    """Modelo que representa un Curso o Bootcamp disponible en la plataforma."""
    TIPO_CHOICES = (
        ('CARRERA', 'Carrera/Bootcamp'),
        ('RELAMPAGO', 'Curso Relámpago'),
    )
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    area = models.ForeignKey(Area, on_delete=models.PROTECT, related_name='cursos')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='CARRERA')
    
    precio_original = models.DecimalField(max_digits=10, decimal_places=0)
    descuento_porcentaje = models.PositiveIntegerField(default=0)
    
    cupos_totales = models.PositiveIntegerField()
    cupos_disponibles = models.PositiveIntegerField()
    
    nivel = models.CharField(max_length=50, blank=True, null=True)
    semanas_duracion = models.PositiveIntegerField(blank=True, null=True)
    cantidad_cursos = models.PositiveIntegerField(blank=True, null=True)
    
    duracion_horas = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    duracion_minutos = models.PositiveIntegerField(blank=True, null=True)

    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True, help_text="Sube una imagen desde tu equipo")
    imagen_url = models.URLField(blank=True, null=True, help_text="O usa una URL de imagen")

    @property
    def get_image(self):
        if self.imagen:
            return self.imagen.url
        return self.imagen_url

    @property
    def precio_final(self):
        return int(float(self.precio_original) * (1 - self.descuento_porcentaje / 100))

    def __str__(self):
        return self.titulo

class CarroMatricula(models.Model):
    """Modelo que representa el carro de compras persistente por usuario."""
    """
    RR - Carro Persistente: ¿Qué es? Es un carro que no vive en cookies temporales, sino en una tabla real de PostgreSQL atado 1 a 1 al Usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carro')
    creado_en = models.DateTimeField(auto_now_add=True)

class ItemCarro(models.Model):
    """Modelo intermedio para guardar los cursos seleccionados en un carro."""
    carro = models.ForeignKey(CarroMatricula, on_delete=models.CASCADE, related_name='items')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('carro', 'curso')

class Matricula(models.Model):
    """Modelo que representa la orden/transacción histórica (Checkout).""" #RR -
    """
    RR - CHOICES: ¿Qué es? Es una regla estricta a nivel de Base de Datos. Evita que escriban estados inventados como "Patata", forzando a elegir opciones predefinidas.
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='matriculas')
    fecha = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    @property
    def codigo(self):
        return f"TRB-{self.fecha.strftime('%y%m')}-{self.id:05d}"

    def __str__(self):
        return f"Matricula {self.codigo} - {self.user.username}"

class DetalleMatricula(models.Model):
    """Modelo para registrar el precio histórico de cada curso al pagar."""
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='detalles')
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=0)
