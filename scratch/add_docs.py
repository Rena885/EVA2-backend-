import os

def add_docstrings(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add docstring to models if not present
    if 'models.py' in filename:
        content = content.replace('class Area(models.Model):', 'class Area(models.Model):\n    """Modelo que representa un Área de Conocimiento."""')
        content = content.replace('class PerfilUsuario(models.Model):', 'class PerfilUsuario(models.Model):\n    """Modelo 1 a 1 con User para manejar roles y tracking de actividad."""')
        content = content.replace('class CarroMatricula(models.Model):', 'class CarroMatricula(models.Model):\n    """Modelo que representa el carro de compras persistente por usuario."""')
        content = content.replace('class Curso(models.Model):', 'class Curso(models.Model):\n    """Modelo que representa un Curso o Bootcamp disponible en la plataforma."""')
        content = content.replace('class ItemCarro(models.Model):', 'class ItemCarro(models.Model):\n    """Modelo intermedio para guardar los cursos seleccionados en un carro."""')
        content = content.replace('class Matricula(models.Model):', 'class Matricula(models.Model):\n    """Modelo que representa la orden/transacción histórica (Checkout)."""')
        content = content.replace('class DetalleMatricula(models.Model):', 'class DetalleMatricula(models.Model):\n    """Modelo para registrar el precio histórico de cada curso al pagar."""')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

add_docstrings('core/models.py')
