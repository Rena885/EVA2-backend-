import os

# Project root: c:\Users\renat\OneDrive\Escritorio\EVA2.0

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# -----------------
# settings.py modifications
# -----------------
# We will append or overwrite settings in a separate step or just rewrite ticketRB/settings.py completely.
# For simplicity, we rewrite settings.py

settings_content = """
import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-dummy-key-for-now'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
    'core',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ticketRB.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ticketRB.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'inacap2026',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'es-cl'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'TOKEN_OBTAIN_SERIALIZER': 'api.serializers.CustomTokenObtainPairSerializer',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'ticketRB API',
    'DESCRIPTION': 'API para plataforma EdTech',
    'VERSION': '1.0.0',
}

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
"""
write_file('ticketRB/settings.py', settings_content)

# -----------------
# core/models.py
# -----------------
models_content = """
from django.db import models
from django.contrib.auth.models import User

class Area(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    ROLES = (
        ('ESTUDIANTE', 'Estudiante'),
        ('COORDINADOR', 'Coordinador'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')

    def __str__(self):
        return f"{self.user.username} - {self.rol}"

class Curso(models.Model):
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

    imagen_url = models.URLField(blank=True, null=True)

    @property
    def precio_final(self):
        return int(self.precio_original * (1 - self.descuento_porcentaje / 100))

    def __str__(self):
        return self.titulo

class CarroMatricula(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='carro')
    creado_en = models.DateTimeField(auto_now_add=True)

class ItemCarro(models.Model):
    carro = models.ForeignKey(CarroMatricula, on_delete=models.CASCADE, related_name='items')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    agregado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('carro', 'curso')

class Matricula(models.Model):
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('PAGADO', 'Pagado'),
        ('CANCELADO', 'Cancelado'),
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='matriculas')
    fecha = models.DateTimeField(auto_now_add=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')

    def __str__(self):
        return f"Matricula {self.id} - {self.user.username}"

class DetalleMatricula(models.Model):
    matricula = models.ForeignKey(Matricula, on_delete=models.CASCADE, related_name='detalles')
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT)
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=0)
"""
write_file('core/models.py', models_content)

# -----------------
# core/signals.py
# -----------------
signals_content = """
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilUsuario, CarroMatricula

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.create(user=instance)
        CarroMatricula.objects.create(user=instance)
"""
write_file('core/signals.py', signals_content)
write_file('core/apps.py', """
from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
""")


# -----------------
# core/forms.py
# -----------------
forms_content = """
from django import forms
from .models import Curso

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }
"""
write_file('core/forms.py', forms_content)

# -----------------
# api/serializers.py
# -----------------
serializers_content = """
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from core.models import Curso, CarroMatricula, ItemCarro, Matricula, DetalleMatricula, Area

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        try:
            token['rol'] = user.perfil.rol
        except Exception:
            token['rol'] = 'ESTUDIANTE'
        return token

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    precio_final = serializers.ReadOnlyField()
    area = AreaSerializer(read_only=True)
    class Meta:
        model = Curso
        fields = '__all__'

class ItemCarroSerializer(serializers.ModelSerializer):
    curso = CursoSerializer(read_only=True)
    curso_id = serializers.PrimaryKeyRelatedField(
        queryset=Curso.objects.all(), source='curso', write_only=True
    )

    class Meta:
        model = ItemCarro
        fields = ['id', 'curso', 'curso_id', 'agregado_en']

class CarroMatriculaSerializer(serializers.ModelSerializer):
    items = ItemCarroSerializer(many=True, read_only=True)
    
    class Meta:
        model = CarroMatricula
        fields = ['id', 'creado_en', 'items']
"""
write_file('api/serializers.py', serializers_content)

# -----------------
# api/permissions.py
# -----------------
permissions_content = """
from rest_framework import permissions

class IsCoordinador(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            hasattr(request.user, 'perfil') and 
            request.user.perfil.rol == 'COORDINADOR'
        )
"""
write_file('api/permissions.py', permissions_content)

# -----------------
# api/views.py
# -----------------
api_views_content = """
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import Curso, CarroMatricula, ItemCarro, Matricula, DetalleMatricula
from .serializers import CursoSerializer, CarroMatriculaSerializer, ItemCarroSerializer
from .permissions import IsCoordinador

class CursoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer

class CarroViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        carro, _ = CarroMatricula.objects.get_or_create(user=request.user)
        serializer = CarroMatriculaSerializer(carro)
        return Response(serializer.data)

class ItemCarroView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCarroSerializer

    def get_queryset(self):
        return ItemCarro.objects.filter(carro__user=self.request.user)

    def perform_create(self, serializer):
        carro, _ = CarroMatricula.objects.get_or_create(user=self.request.user)
        curso = serializer.validated_data['curso']
        if ItemCarro.objects.filter(carro=carro, curso=curso).exists():
            raise serializers.ValidationError({"detail": "El curso ya está en el carro."})
        serializer.save(carro=carro)

class ItemCarroDetailView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ItemCarroSerializer
    
    def get_queryset(self):
        return ItemCarro.objects.filter(carro__user=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):
    user = request.user
    carro = get_object_or_404(CarroMatricula, user=user)
    items = carro.items.all()
    
    if not items.exists():
        return Response({'detail': 'El carro está vacío.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            costo_total = 0
            # Validar cupos y calcular total (NO STOCK HOARDING)
            for item in items:
                # Select for update para prevenir condiciones de carrera
                curso = Curso.objects.select_for_update().get(id=item.curso.id)
                if curso.cupos_disponibles <= 0:
                    raise ValueError(f'No hay cupos disponibles para: {curso.titulo}')
                costo_total += curso.precio_final
            
            # Crear matrícula
            matricula = Matricula.objects.create(
                user=user,
                costo_total=costo_total,
                estado='PAGADO' # Asumimos pago inmediato para el ejercicio
            )
            
            # Procesar items
            for item in items:
                curso = Curso.objects.select_for_update().get(id=item.curso.id)
                curso.cupos_disponibles -= 1
                curso.save()
                
                DetalleMatricula.objects.create(
                    matricula=matricula,
                    curso=curso,
                    precio_pagado=curso.precio_final
                )
            
            # Vaciar carro
            carro.items.all().delete()
            
        return Response({'detail': 'Matrícula exitosa', 'matricula_id': matricula.id}, status=status.HTTP_201_CREATED)
    
    except ValueError as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsCoordinador])
def cancelar_matricula(request, pk):
    try:
        with transaction.atomic():
            matricula = get_object_or_404(Matricula.objects.select_for_update(), pk=pk)
            if matricula.estado == 'CANCELADO':
                return Response({'detail': 'Ya está cancelada.'}, status=status.HTTP_400_BAD_REQUEST)
            
            matricula.estado = 'CANCELADO'
            matricula.save()
            
            # Reponer stock
            for detalle in matricula.detalles.all():
                curso = Curso.objects.select_for_update().get(id=detalle.curso.id)
                curso.cupos_disponibles += 1
                curso.save()
                
        return Response({'detail': 'Matrícula cancelada y cupos repuestos.'})
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
"""
write_file('api/views.py', api_views_content)

# -----------------
# api/urls.py
# -----------------
api_urls_content = """
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
    # Auth
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Carro
    path('carro/', views.CarroViewSet.as_view({'get': 'list'}), name='carro-list'),
    path('carro/items/', views.ItemCarroView.as_view(), name='carro-items'),
    path('carro/items/<int:pk>/', views.ItemCarroDetailView.as_view(), name='carro-item-detail'),
    path('carro/checkout/', views.checkout, name='checkout'),
    
    # Panel Admin
    path('matriculas/<int:pk>/cancelar/', views.cancelar_matricula, name='cancelar-matricula'),
    
    # Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
"""
write_file('api/urls.py', api_urls_content)

# -----------------
# core/views.py (UI / Templates)
# -----------------
core_views_content = """
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Curso, Area, Matricula, DetalleMatricula
from .forms import CursoForm
from django.contrib import messages

def home(request):
    cursos_destacados = Curso.objects.filter(cupos_disponibles__gt=0)[:3]
    return render(request, 'home.html', {'cursos': cursos_destacados})

def catalogo(request):
    area_id = request.GET.get('area')
    q = request.GET.get('q')
    
    cursos = Curso.objects.all()
    if area_id:
        cursos = cursos.filter(area_id=area_id)
    if q:
        cursos = cursos.filter(titulo__icontains=q)
        
    areas = Area.objects.all()
    
    carreras = cursos.filter(tipo='CARRERA')
    relampagos = cursos.filter(tipo='RELAMPAGO')
    
    return render(request, 'catalogo.html', {
        'carreras': carreras,
        'relampagos': relampagos,
        'areas': areas,
        'selected_area': int(area_id) if area_id else None
    })

@login_required
def carro_view(request):
    return render(request, 'carro.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.perfil.rol == 'COORDINADOR':
            return redirect('panel')
        return redirect('catalogo')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.perfil.rol == 'COORDINADOR':
                return redirect('panel')
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('catalogo')
    else:
        form = UserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

# PANEL DE COORDINADOR
@login_required
def panel_view(request):
    if request.user.perfil.rol != 'COORDINADOR':
        return redirect('home')
        
    cursos = Curso.objects.all()
    matriculas = Matricula.objects.all().order_by('-fecha')
    
    return render(request, 'panel/dashboard.html', {
        'cursos': cursos,
        'matriculas': matriculas
    })

@login_required
def panel_curso_crear(request):
    if request.user.perfil.rol != 'COORDINADOR':
        return redirect('home')
        
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso creado con éxito.')
            return redirect('panel')
    else:
        form = CursoForm()
    return render(request, 'panel/curso_form.html', {'form': form, 'title': 'Crear Curso'})

@login_required
def panel_curso_editar(request, pk):
    if request.user.perfil.rol != 'COORDINADOR':
        return redirect('home')
        
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado con éxito.')
            return redirect('panel')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'panel/curso_form.html', {'form': form, 'title': 'Editar Curso'})

@login_required
def panel_curso_eliminar(request, pk):
    if request.user.perfil.rol != 'COORDINADOR':
        return redirect('home')
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('panel')
    return render(request, 'panel/curso_confirm_delete.html', {'curso': curso})
"""
write_file('core/views.py', core_views_content)

# -----------------
# ticketRB/urls.py
# -----------------
main_urls_content = """
from django.urls import path, include
from core import views

urlpatterns = [
    # API
    path('api/', include('api.urls')),
    
    # Vistas UI
    path('', views.home, name='home'),
    path('cursos/', views.catalogo, name='catalogo'),
    path('carro/', views.carro_view, name='carro'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', include('django.contrib.auth.urls')), # Usará views base
    
    # Panel Admin
    path('panel/', views.panel_view, name='panel'),
    path('panel/curso/nuevo/', views.panel_curso_crear, name='panel_curso_crear'),
    path('panel/curso/<int:pk>/editar/', views.panel_curso_editar, name='panel_curso_editar'),
    path('panel/curso/<int:pk>/eliminar/', views.panel_curso_eliminar, name='panel_curso_eliminar'),
]
"""
write_file('ticketRB/urls.py', main_urls_content)

# TEMPLATES
templates = {
    'home.html': """{% extends 'base.html' %}
{% block content %}
<div class="container-fluid p-0 bg-dark text-white mb-5" style="background: linear-gradient(135deg, #111 0%, #333 100%);">
    <div class="container py-5 text-center">
        <h1 class="display-3 fw-bold mb-3 mt-5">Potencia tu futuro con ticket<span style="color: var(--accent);">RB</span></h1>
        <p class="lead mb-4 fw-light" style="max-width: 600px; margin: 0 auto;">Cursos, bootcamps y micro-formaciones en tecnología y diseño. Aprende a tu ritmo con los mejores profesionales.</p>
        <a href="{% url 'catalogo' %}" class="btn btn-accent btn-lg px-5 mb-5 rounded-pill shadow-lg">Explora nuestros cursos</a>
    </div>
</div>

<div class="container mb-5">
    <div class="text-center mb-5">
        <h2 class="fw-bold">Nuestra Propuesta</h2>
        <p class="text-muted">Metodología práctica orientada al mercado laboral</p>
    </div>
    <div class="row g-4 text-center">
        <div class="col-md-4">
            <div class="p-4 bg-white rounded-4 shadow-sm h-100">
                <i class="bi bi-laptop fs-1 text-primary mb-3"></i>
                <h4 class="fw-bold">Clases en Vivo</h4>
                <p class="text-muted small">Interactúa con profesores y tutores en tiempo real.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="p-4 bg-white rounded-4 shadow-sm h-100">
                <i class="bi bi-briefcase fs-1 text-success mb-3"></i>
                <h4 class="fw-bold">Proyectos Reales</h4>
                <p class="text-muted small">Arma tu portafolio con casos de estudio del mundo real.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="p-4 bg-white rounded-4 shadow-sm h-100">
                <i class="bi bi-people fs-1 text-warning mb-3"></i>
                <h4 class="fw-bold">Comunidad</h4>
                <p class="text-muted small">Haz networking con miles de estudiantes de toda la región.</p>
            </div>
        </div>
    </div>
</div>

<div class="container mb-5 pb-5">
    <div class="d-flex justify-content-between align-items-end mb-4">
        <h2 class="fw-bold mb-0">Cursos Destacados</h2>
        <a href="{% url 'catalogo' %}" class="text-decoration-none fw-semibold">Ver todos los cursos &rarr;</a>
    </div>
    
    <div class="row g-4">
        {% for curso in cursos %}
        <div class="col-md-4">
            <div class="card course-card">
                {% if curso.imagen_url %}
                    <img src="{{ curso.imagen_url }}" class="card-img-top" alt="{{ curso.titulo }}">
                {% else %}
                    <div class="card-img-top d-flex align-items-center justify-content-center bg-light">
                        <i class="bi bi-image text-muted fs-1"></i>
                    </div>
                {% endif %}
                <span class="course-badge text-dark">{{ curso.area.nombre }}</span>
                <div class="card-body p-4 d-flex flex-column">
                    <h5 class="card-title fw-bold">{{ curso.titulo }}</h5>
                    <p class="card-text text-muted small mb-4">{{ curso.descripcion|truncatewords:15 }}</p>
                    
                    <div class="mt-auto">
                        {% if curso.descuento_porcentaje > 0 %}
                            <div class="d-flex align-items-center mb-1">
                                <span class="price-original me-2">${{ curso.precio_original }}</span>
                                <span class="discount-tag">{{ curso.descuento_porcentaje }}% OFF</span>
                            </div>
                        {% endif %}
                        <div class="d-flex justify-content-between align-items-center">
                            <span class="price-final">${{ curso.precio_final }}</span>
                            <form method="POST" action="javascript:void(0);">
                                {% csrf_token %}
                                <button type="button" class="btn btn-dark rounded-pill px-3 add-to-cart-btn" data-course-id="{{ curso.id }}">
                                    Agregar <i class="bi bi-cart-plus ms-1"></i>
                                </button>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}
    """,
    'catalogo.html': """{% extends 'base.html' %}
{% block title %}Catálogo - ticketRB{% endblock %}
{% block content %}
<div class="bg-dark text-white py-4 mb-4">
    <div class="container">
        <h2 class="fw-bold m-0">Catálogo de Cursos</h2>
    </div>
</div>

<div class="container mb-5">
    <div class="row">
        <!-- Filtros -->
        <div class="col-lg-3 mb-4">
            <div class="bg-white p-4 rounded-4 shadow-sm sticky-top" style="top: 100px;">
                <h5 class="fw-bold mb-3">Categorías</h5>
                <div class="list-group list-group-flush">
                    <a href="{% url 'catalogo' %}" class="list-group-item list-group-item-action {% if not selected_area %}active fw-bold border-0 bg-light{% else %}border-0{% endif %} rounded mb-1">Todas</a>
                    {% for area in areas %}
                        <a href="?area={{ area.id }}" class="list-group-item list-group-item-action {% if selected_area == area.id %}active fw-bold border-0 bg-light text-dark{% else %}border-0{% endif %} rounded mb-1">{{ area.nombre }}</a>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <!-- Listado -->
        <div class="col-lg-9">
            
            {% if carreras %}
            <div class="mb-5">
                <h3 class="fw-bold mb-4 border-bottom pb-2">Carreras & Bootcamps <span class="badge bg-secondary fs-6 rounded-pill ms-2 fw-normal">{{ carreras|length }}</span></h3>
                <div class="row g-4">
                    {% for curso in carreras %}
                    <div class="col-md-6">
                        <div class="card course-card border border-light">
                            {% if curso.imagen_url %}
                                <img src="{{ curso.imagen_url }}" class="card-img-top" alt="{{ curso.titulo }}">
                            {% else %}
                                <div class="card-img-top d-flex align-items-center justify-content-center bg-light">
                                    <i class="bi bi-book text-muted fs-1"></i>
                                </div>
                            {% endif %}
                            <span class="course-badge text-dark"><i class="bi bi-star-fill text-warning me-1"></i> Bootcamp</span>
                            
                            <div class="card-body p-4 d-flex flex-column">
                                <h5 class="card-title fw-bold">{{ curso.titulo }}</h5>
                                <div class="mb-3 d-flex gap-2 flex-wrap text-muted small">
                                    {% if curso.nivel %}<span><i class="bi bi-bar-chart-fill"></i> {{ curso.nivel }}</span> &bull;{% endif %}
                                    {% if curso.semanas_duracion %}<span><i class="bi bi-calendar3"></i> {{ curso.semanas_duracion }} Semanas</span> &bull;{% endif %}
                                    {% if curso.cantidad_cursos %}<span><i class="bi bi-collection"></i> {{ curso.cantidad_cursos }} Cursos</span>{% endif %}
                                </div>
                                <p class="card-text text-muted small mb-4">{{ curso.descripcion|truncatewords:15 }}</p>
                                
                                <div class="mt-auto pt-3 border-top">
                                    {% if curso.descuento_porcentaje > 0 %}
                                        <div class="d-flex align-items-center mb-1">
                                            <span class="price-original me-2">${{ curso.precio_original }}</span>
                                            <span class="discount-tag">{{ curso.descuento_porcentaje }}% OFF</span>
                                        </div>
                                    {% endif %}
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <span class="price-final fs-4">${{ curso.precio_final }}</span>
                                    </div>
                                    <form method="POST" action="javascript:void(0);" class="d-grid">
                                        {% csrf_token %}
                                        <button type="button" class="btn btn-warning fw-bold rounded-3 py-2 add-to-cart-btn text-dark" data-course-id="{{ curso.id }}">
                                            Ver carrera e Inscribirse <i class="bi bi-arrow-right ms-1"></i>
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if relampagos %}
            <div>
                <div class="d-flex align-items-center mb-4 border-bottom pb-2">
                    <h3 class="fw-bold m-0"><i class="bi bi-lightning-charge-fill text-warning"></i> Cursos Relámpago</h3>
                    <span class="badge bg-secondary fs-6 rounded-pill ms-3 fw-normal">{{ relampagos|length }}</span>
                </div>
                <div class="alert alert-info border-0 bg-info bg-opacity-10 shadow-sm rounded-3 mb-4">
                    <i class="bi bi-info-circle-fill me-2"></i> <strong>Cursos Relámpago:</strong> Aprende una habilidad específica en pocas horas. Sin compromisos a largo plazo, directos al grano.
                </div>
                
                <div class="row g-4">
                    {% for curso in relampagos %}
                    <div class="col-md-4">
                        <div class="card course-card">
                            {% if curso.imagen_url %}
                                <img src="{{ curso.imagen_url }}" class="card-img-top" style="height: 140px;" alt="{{ curso.titulo }}">
                            {% else %}
                                <div class="card-img-top d-flex align-items-center justify-content-center bg-light" style="height: 140px;">
                                    <i class="bi bi-lightning text-muted fs-1"></i>
                                </div>
                            {% endif %}
                            <span class="course-badge text-dark bg-warning border border-warning"><i class="bi bi-lightning-fill"></i> Relámpago</span>
                            
                            <div class="card-body p-3 d-flex flex-column">
                                <h6 class="card-title fw-bold">{{ curso.titulo }}</h6>
                                <div class="mb-2 text-muted" style="font-size: 0.75rem;">
                                    {% if curso.duracion_horas %}<span><i class="bi bi-clock"></i> {{ curso.duracion_horas }} Hrs</span>{% endif %}
                                    {% if curso.duracion_minutos %}<span><i class="bi bi-clock"></i> {{ curso.duracion_minutos }} Min</span>{% endif %}
                                </div>
                                
                                <div class="mt-auto pt-2 border-top">
                                    {% if curso.descuento_porcentaje > 0 %}
                                        <div class="d-flex align-items-center mb-1">
                                            <span class="price-original me-2" style="font-size: 0.7rem;">${{ curso.precio_original }}</span>
                                            <span class="discount-tag py-0 px-1" style="font-size: 0.65rem;">{{ curso.descuento_porcentaje }}% OFF</span>
                                        </div>
                                    {% endif %}
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span class="price-final fs-5">${{ curso.precio_final }}</span>
                                    </div>
                                    <form method="POST" action="javascript:void(0);" class="d-grid">
                                        {% csrf_token %}
                                        <button type="button" class="btn btn-dark btn-sm fw-bold rounded-2 add-to-cart-btn" data-course-id="{{ curso.id }}">
                                            Inscribirme
                                        </button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}

            {% if not carreras and not relampagos %}
            <div class="text-center py-5">
                <i class="bi bi-search text-muted" style="font-size: 3rem;"></i>
                <h4 class="mt-3 fw-bold">No encontramos cursos</h4>
                <p class="text-muted">Intenta con otra categoría o término de búsqueda.</p>
                <a href="{% url 'catalogo' %}" class="btn btn-outline-dark mt-2">Limpiar filtros</a>
            </div>
            {% endif %}
            
        </div>
    </div>
</div>
{% endblock %}
    """,
    'carro.html': """{% extends 'base.html' %}
{% block title %}Mi Carrito - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <h2 class="fw-bold mb-4">Finalizar Compra</h2>
    
    <div class="row" id="cart-container">
        <!-- Generado por JS -->
        <div class="col-12 text-center py-5" id="cart-loading">
            <div class="spinner-border text-primary" role="status"></div>
            <p class="mt-2 text-muted">Cargando tu carrito...</p>
        </div>
    </div>
</div>

{% csrf_token %}
{% endblock %}

{% block extra_js %}
<script>
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    async function loadCart() {
        try {
            const res = await fetch('/api/carro/');
            if(res.ok) {
                const data = await res.json();
                renderCart(data);
            } else {
                showToast('Error cargando el carrito', 'error');
            }
        } catch(e) {
            console.error(e);
            showToast('Error de conexión', 'error');
        }
    }
    
    function renderCart(cartData) {
        const container = document.getElementById('cart-container');
        if(!cartData.items || cartData.items.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center py-5 bg-white rounded-4 shadow-sm border border-light">
                    <i class="bi bi-cart-x text-muted" style="font-size: 4rem;"></i>
                    <h4 class="mt-3 fw-bold">Tu carrito está vacío</h4>
                    <p class="text-muted">¡Descubre nuestros cursos y potencia tu carrera!</p>
                    <a href="/cursos/" class="btn btn-accent px-4 py-2 mt-3 fw-bold">Explorar Cursos</a>
                </div>
            `;
            return;
        }
        
        let total = 0;
        let itemsHtml = '<div class="col-lg-8 mb-4"><div class="bg-white rounded-4 shadow-sm p-4 border border-light">';
        itemsHtml += '<h5 class="fw-bold mb-4 border-bottom pb-3">Resumen de cursos</h5>';
        
        cartData.items.forEach(item => {
            const curso = item.curso;
            total += curso.precio_final;
            
            itemsHtml += `
                <div class="d-flex align-items-center mb-4 pb-3 border-bottom position-relative">
                    <img src="${curso.imagen_url || 'https://via.placeholder.com/100'}" class="rounded-3 me-3" style="width: 80px; height: 80px; object-fit: cover;">
                    <div class="flex-grow-1">
                        <h6 class="fw-bold mb-1">${curso.titulo}</h6>
                        <p class="text-muted small mb-0">${curso.tipo === 'CARRERA' ? 'Carrera / Bootcamp' : 'Curso Relámpago'}</p>
                        ${curso.cupos_disponibles <= 0 ? '<span class="badge bg-danger mt-1">Sin cupos</span>' : `<span class="text-success small"><i class="bi bi-check-circle-fill"></i> Cupos disponibles</span>`}
                    </div>
                    <div class="text-end">
                        <div class="fw-bold fs-5 mb-1">$${curso.precio_final}</div>
                        <button class="btn btn-sm text-danger p-0 delete-item" data-id="${item.id}">
                            <i class="bi bi-trash3"></i> Eliminar
                        </button>
                    </div>
                </div>
            `;
        });
        
        itemsHtml += '</div></div>';
        
        // Checkout Box
        let checkoutHtml = `
            <div class="col-lg-4">
                <div class="bg-white rounded-4 shadow-sm p-4 border border-light sticky-top" style="top: 100px;">
                    <h5 class="fw-bold mb-4">Total a pagar</h5>
                    <div class="d-flex justify-content-between mb-3">
                        <span class="text-muted">Subtotal</span>
                        <span class="fw-bold">$${total}</span>
                    </div>
                    <hr>
                    <div class="d-flex justify-content-between mb-4">
                        <span class="fw-bold fs-5">Total</span>
                        <span class="fw-bold fs-4 text-primary">$${total}</span>
                    </div>
                    <button class="btn btn-dark w-100 py-3 fw-bold rounded-3" id="checkout-btn">
                        Pagar e Inscribirme <i class="bi bi-lock-fill ms-1"></i>
                    </button>
                    <p class="text-center text-muted small mt-3 mb-0"><i class="bi bi-shield-check text-success"></i> Pago seguro. No retenemos cupos hasta confirmar.</p>
                </div>
            </div>
        `;
        
        container.innerHTML = itemsHtml + checkoutHtml;
        
        // Attach listeners
        document.querySelectorAll('.delete-item').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const itemId = e.target.closest('button').dataset.id;
                try {
                    const res = await fetch(`/api/carro/items/${itemId}/`, {
                        method: 'DELETE',
                        headers: {'X-CSRFToken': csrfToken}
                    });
                    if(res.ok) {
                        showToast('Curso eliminado del carrito');
                        loadCart();
                        // Update counter
                        const cartRes = await fetch(`/api/carro/`);
                        if (cartRes.ok) {
                            const cartData = await cartRes.json();
                            updateCartCounter(cartData.items.length);
                        }
                    }
                } catch(err) {
                    showToast('Error eliminando', 'error');
                }
            });
        });
        
        document.getElementById('checkout-btn').addEventListener('click', async () => {
            const btn = document.getElementById('checkout-btn');
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Procesando...';
            
            try {
                const res = await fetch('/api/carro/checkout/', {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrfToken}
                });
                
                const data = await res.json();
                
                if(res.ok) {
                    container.innerHTML = `
                        <div class="col-12 text-center py-5 bg-white rounded-4 shadow-sm border border-light">
                            <i class="bi bi-check-circle-fill text-success" style="font-size: 5rem;"></i>
                            <h2 class="mt-3 fw-bold">¡Inscripción Exitosa!</h2>
                            <p class="text-muted lead">Te has matriculado correctamente. ID de transacción: #${data.matricula_id}</p>
                            <a href="/cursos/" class="btn btn-outline-dark px-4 py-2 mt-3 fw-bold">Volver al catálogo</a>
                        </div>
                    `;
                    updateCartCounter(0);
                    showToast('Pago procesado correctamente', 'success');
                } else {
                    showToast(data.detail || 'Error en el pago', 'error');
                    btn.disabled = false;
                    btn.innerHTML = 'Pagar e Inscribirme <i class="bi bi-lock-fill ms-1"></i>';
                }
            } catch(err) {
                showToast('Error de red durante el pago', 'error');
                btn.disabled = false;
                btn.innerHTML = 'Pagar e Inscribirme <i class="bi bi-lock-fill ms-1"></i>';
            }
        });
    }
    
    document.addEventListener('DOMContentLoaded', loadCart);
</script>
{% endblock %}
    """,
    'auth/login.html': """{% extends 'base.html' %}
{% block title %}Iniciar Sesión - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-5">
            <div class="card border-0 shadow-sm rounded-4 p-4">
                <div class="text-center mb-4">
                    <h3 class="fw-bold">Bienvenido de vuelta</h3>
                    <p class="text-muted">Ingresa a tu cuenta de ticketRB</p>
                </div>
                <form method="POST">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-dark w-100 py-2 fw-bold mt-3">Ingresar</button>
                </form>
                <div class="text-center mt-4 pt-3 border-top">
                    <p class="text-muted small">¿No tienes cuenta? <a href="{% url 'register' %}" class="fw-bold text-dark text-decoration-none">Regístrate aquí</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",
    'auth/register.html': """{% extends 'base.html' %}
{% block title %}Registro - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card border-0 shadow-sm rounded-4 p-4">
                <div class="text-center mb-4">
                    <h3 class="fw-bold">Crea tu cuenta</h3>
                    <p class="text-muted">Únete a la plataforma líder en EdTech</p>
                </div>
                <form method="POST">
                    {% csrf_token %}
                    {{ form.as_p }}
                    <button type="submit" class="btn btn-accent w-100 py-2 fw-bold mt-3">Registrarme</button>
                </form>
                <div class="text-center mt-4 pt-3 border-top">
                    <p class="text-muted small">¿Ya tienes cuenta? <a href="{% url 'login' %}" class="fw-bold text-dark text-decoration-none">Ingresa aquí</a></p>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}""",
    'panel/dashboard.html': """{% extends 'base.html' %}
{% block title %}Panel Admin - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-5">
        <div>
            <h2 class="fw-bold m-0">Panel de Coordinación</h2>
            <p class="text-muted mb-0">Gestión de cursos y matrículas</p>
        </div>
        <a href="{% url 'panel_curso_crear' %}" class="btn btn-dark"><i class="bi bi-plus-circle me-2"></i>Nuevo Curso</a>
    </div>

    {% if messages %}
    <div class="mb-4">
        {% for message in messages %}
        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <div class="row mb-5">
        <div class="col-md-4">
            <div class="bg-white p-4 rounded-4 shadow-sm border-start border-primary border-4">
                <div class="text-muted small fw-bold mb-1">TOTAL CURSOS</div>
                <h3 class="fw-bold m-0">{{ cursos.count }}</h3>
            </div>
        </div>
        <div class="col-md-4">
            <div class="bg-white p-4 rounded-4 shadow-sm border-start border-success border-4">
                <div class="text-muted small fw-bold mb-1">MATRÍCULAS PAGADAS</div>
                <h3 class="fw-bold m-0">{{ matriculas.count }}</h3>
            </div>
        </div>
    </div>

    <!-- Nav tabs -->
    <ul class="nav nav-tabs mb-4" id="adminTabs" role="tablist">
        <li class="nav-item" role="presentation">
            <button class="nav-link active fw-bold text-dark" id="cursos-tab" data-bs-toggle="tab" data-bs-target="#cursos" type="button" role="tab">Gestión de Cursos</button>
        </li>
        <li class="nav-item" role="presentation">
            <button class="nav-link fw-bold text-dark" id="matriculas-tab" data-bs-toggle="tab" data-bs-target="#matriculas" type="button" role="tab">Matrículas Recientes</button>
        </li>
    </ul>

    <!-- Tab panes -->
    <div class="tab-content" id="adminTabsContent">
        <div class="tab-pane fade show active" id="cursos" role="tabpanel">
            <div class="bg-white rounded-4 shadow-sm overflow-hidden">
                <div class="table-responsive">
                    <table class="table table-hover align-middle m-0">
                        <thead class="table-light">
                            <tr>
                                <th>ID</th>
                                <th>Curso</th>
                                <th>Tipo</th>
                                <th>Cupos</th>
                                <th>Precio Final</th>
                                <th class="text-end">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for c in cursos %}
                            <tr>
                                <td class="text-muted">#{{ c.id }}</td>
                                <td><span class="fw-semibold">{{ c.titulo }}</span><br><small class="text-muted">{{ c.area.nombre }}</small></td>
                                <td>
                                    {% if c.tipo == 'CARRERA' %}
                                    <span class="badge bg-light text-dark border"><i class="bi bi-star-fill text-warning"></i> Bootcamp</span>
                                    {% else %}
                                    <span class="badge bg-warning text-dark border border-warning"><i class="bi bi-lightning-fill"></i> Relámpago</span>
                                    {% endif %}
                                </td>
                                <td>
                                    <div class="progress" style="height: 6px; width: 80px;" title="{{ c.cupos_disponibles }} / {{ c.cupos_totales }}">
                                        {% widthratio c.cupos_disponibles c.cupos_totales 100 as pct %}
                                        <div class="progress-bar {% if pct|add:0 < 20 %}bg-danger{% else %}bg-success{% endif %}" style="width: {{ pct }}%"></div>
                                    </div>
                                    <small class="text-muted">{{ c.cupos_disponibles }}/{{ c.cupos_totales }}</small>
                                </td>
                                <td class="fw-bold">${{ c.precio_final }}</td>
                                <td class="text-end">
                                    <a href="{% url 'panel_curso_editar' c.id %}" class="btn btn-sm btn-outline-primary"><i class="bi bi-pencil"></i></a>
                                    <a href="{% url 'panel_curso_eliminar' c.id %}" class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></a>
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <div class="tab-pane fade" id="matriculas" role="tabpanel">
            <div class="bg-white rounded-4 shadow-sm overflow-hidden">
                <div class="table-responsive">
                    <table class="table table-hover align-middle m-0">
                        <thead class="table-light">
                            <tr>
                                <th>Transacción</th>
                                <th>Usuario</th>
                                <th>Fecha</th>
                                <th>Total</th>
                                <th>Estado</th>
                                <th class="text-end">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for m in matriculas %}
                            <tr>
                                <td class="fw-bold">#{{ m.id }}</td>
                                <td>{{ m.user.username }}</td>
                                <td>{{ m.fecha|date:"d M Y, H:i" }}</td>
                                <td class="fw-semibold">${{ m.costo_total }}</td>
                                <td>
                                    {% if m.estado == 'PAGADO' %}
                                        <span class="badge bg-success">Pagado</span>
                                    {% elif m.estado == 'CANCELADO' %}
                                        <span class="badge bg-danger">Cancelado</span>
                                    {% else %}
                                        <span class="badge bg-warning text-dark">Pendiente</span>
                                    {% endif %}
                                </td>
                                <td class="text-end">
                                    {% if m.estado != 'CANCELADO' %}
                                    <button class="btn btn-sm btn-outline-danger btn-cancel-matricula" data-id="{{ m.id }}" title="Cancelar y reponer cupos">
                                        <i class="bi bi-x-circle"></i> Cancelar
                                    </button>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                            {% if not matriculas %}
                            <tr><td colspan="6" class="text-center py-4 text-muted">No hay matrículas registradas.</td></tr>
                            {% endif %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% csrf_token %}
{% endblock %}

{% block extra_js %}
<script>
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    document.querySelectorAll('.btn-cancel-matricula').forEach(btn => {
        btn.addEventListener('click', async (e) => {
            if(!confirm('¿Estás seguro de cancelar esta matrícula? Los cupos serán repuestos automáticamente.')) return;
            
            const mId = e.target.closest('button').dataset.id;
            try {
                const res = await fetch(`/api/matriculas/${mId}/cancelar/`, {
                    method: 'POST',
                    headers: {'X-CSRFToken': csrfToken}
                });
                const data = await res.json();
                
                if(res.ok) {
                    showToast('Matrícula cancelada correctamente', 'success');
                    setTimeout(() => window.location.reload(), 1500);
                } else {
                    showToast(data.detail || 'Error al cancelar', 'error');
                }
            } catch(e) {
                showToast('Error de red', 'error');
            }
        });
    });
</script>
{% endblock %}""",
    'panel/curso_form.html': """{% extends 'base.html' %}
{% block title %}{{ title }} - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h3 class="fw-bold m-0">{{ title }}</h3>
                <a href="{% url 'panel' %}" class="btn btn-outline-secondary btn-sm"><i class="bi bi-arrow-left"></i> Volver</a>
            </div>
            
            <div class="card border-0 shadow-sm rounded-4">
                <div class="card-body p-4">
                    <form method="POST">
                        {% csrf_token %}
                        <div class="row">
                            {% for field in form %}
                                <div class="col-md-{% if field.name in 'descripcion' %}12{% elif field.name in 'titulo,imagen_url' %}12{% else %}6{% endif %} mb-3">
                                    <label class="form-label fw-bold text-muted small">{{ field.label }}</label>
                                    {{ field }}
                                    {% if field.help_text %}
                                        <div class="form-text">{{ field.help_text }}</div>
                                    {% endif %}
                                    {% if field.errors %}
                                        <div class="text-danger small">{{ field.errors }}</div>
                                    {% endif %}
                                </div>
                            {% endfor %}
                        </div>
                        <div class="mt-4 pt-3 border-top text-end">
                            <button type="submit" class="btn btn-dark fw-bold px-4">Guardar Curso</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    // Agregar clases de bootstrap a los inputs del form
    document.addEventListener("DOMContentLoaded", function() {
        document.querySelectorAll('input, select, textarea').forEach(el => {
            if(el.type !== 'checkbox' && el.type !== 'hidden') {
                el.classList.add('form-control');
            }
            if(el.type === 'checkbox') {
                el.classList.add('form-check-input');
            }
        });
    });
</script>
{% endblock %}""",
    'panel/curso_confirm_delete.html': """{% extends 'base.html' %}
{% block title %}Eliminar Curso - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="row justify-content-center">
        <div class="col-md-6 text-center">
            <div class="card border-0 shadow-sm rounded-4 p-5">
                <i class="bi bi-exclamation-triangle-fill text-warning" style="font-size: 4rem;"></i>
                <h3 class="fw-bold mt-3">¿Eliminar Curso?</h3>
                <p class="text-muted">Estás a punto de eliminar el curso <strong>"{{ curso.titulo }}"</strong>. Esta acción no se puede deshacer.</p>
                
                <form method="POST" class="mt-4">
                    {% csrf_token %}
                    <a href="{% url 'panel' %}" class="btn btn-outline-secondary me-2">Cancelar</a>
                    <button type="submit" class="btn btn-danger fw-bold">Sí, eliminar</button>
                </form>
            </div>
        </div>
    </div>
</div>
{% endblock %}"""
}

for rel_path, content in templates.items():
    write_file(f"templates/{rel_path}", content)

# -----------------
# core/management/commands/seed_data.py
# -----------------
seed_script = '''
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Area, Curso, PerfilUsuario

class Command(BaseCommand):
    help = "Limpia y puebla la base de datos con las 7 categorías, 3 carreras y 2 cursos relámpagos por cada una (Total 35)."

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("Limpiando datos..."))
        Curso.objects.all().delete()
        Area.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()
        
        # 1. Crear Coordinador de Prueba
        admin_user = User.objects.create_user('coordinador', 'admin@ticketrb.cl', 'admin123')
        # La señal crea el perfil automáticamente con rol ESTUDIANTE. Lo actualizamos a COORDINADOR.
        admin_user.perfil.rol = 'COORDINADOR'
        admin_user.perfil.save()
        
        # 2. Categorías
        nombres_areas = [
            "Data", 
            "Diseño UX/UI", 
            "Inteligencia Artificial", 
            "Marketing Digital", 
            "Negocios", 
            "Producto", 
            "Programación y Desarrollo"
        ]
        
        areas = {}
        for n in nombres_areas:
            areas[n] = Area.objects.create(nombre=n)
        
        self.stdout.write(self.style.SUCCESS(f"{len(areas)} Áreas creadas."))

        # 3. Poblamiento de Cursos
        # 7 áreas * (3 Carreras + 2 Relámpagos) = 35 cursos
        
        cursos_data = [
            # Data
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Science Bootcamp", "precio": 1500000, "desc": 20, "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Analytics Advanced", "precio": 1200000, "desc": 15, "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "CARRERA", "titulo": "Data Engineering en Cloud", "precio": 1600000, "desc": 25, "img": "https://images.unsplash.com/photo-1504868584819-f8e8b4b6d7e3?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "RELAMPAGO", "titulo": "SQL para Principiantes", "precio": 45000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Data", "tipo": "RELAMPAGO", "titulo": "PowerBI Express", "precio": 50000, "desc": 70, "horas": 6, "img": "https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=500&q=60"},
            
            # Diseño UX/UI
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "Carrera Diseño UX/UI", "precio": 1300000, "desc": 30, "img": "https://images.unsplash.com/photo-1561070791-2526d30994b5?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "Product Design", "precio": 1400000, "desc": 20, "img": "https://images.unsplash.com/photo-1586717791821-3f44a563fa4c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "CARRERA", "titulo": "UI Engineering", "precio": 1100000, "desc": 10, "img": "https://images.unsplash.com/photo-1618761714954-0b8cd0026356?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "RELAMPAGO", "titulo": "Figma Masterclass", "precio": 35000, "desc": 40, "horas": 3, "img": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&w=500&q=60"},
            {"area": "Diseño UX/UI", "tipo": "RELAMPAGO", "titulo": "Microinteracciones con Framer", "precio": 40000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1626785774573-4b799315345d?auto=format&fit=crop&w=500&q=60"},
            
            # Inteligencia Artificial
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "Machine Learning Engineer", "precio": 1800000, "desc": 20, "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "AI for Business", "precio": 1500000, "desc": 15, "img": "https://images.unsplash.com/photo-1678120000676-47b192ea60c9?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "CARRERA", "titulo": "Deep Learning Bootcamp", "precio": 1900000, "desc": 30, "img": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "RELAMPAGO", "titulo": "Prompt Engineering Avanzado", "precio": 25000, "desc": 60, "horas": 2, "img": "https://images.unsplash.com/photo-1678911820864-e2c567c655d7?auto=format&fit=crop&w=500&q=60"},
            {"area": "Inteligencia Artificial", "tipo": "RELAMPAGO", "titulo": "Chatbots con LangChain", "precio": 55000, "desc": 40, "horas": 5, "img": "https://images.unsplash.com/photo-1679083216051-aa510a1a2c0e?auto=format&fit=crop&w=500&q=60"},
            
            # Marketing Digital
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Growth Marketing", "precio": 1200000, "desc": 40, "img": "https://images.unsplash.com/photo-1432888498266-38ffec3eaf0a?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Performance Marketing", "precio": 1100000, "desc": 20, "img": "https://images.unsplash.com/photo-1533750349088-cd871a92f312?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "CARRERA", "titulo": "Content Manager", "precio": 900000, "desc": 15, "img": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "RELAMPAGO", "titulo": "TikTok Ads", "precio": 30000, "desc": 70, "horas": 3, "img": "https://images.unsplash.com/photo-1611162616475-46b635cb6868?auto=format&fit=crop&w=500&q=60"},
            {"area": "Marketing Digital", "tipo": "RELAMPAGO", "titulo": "SEO Técnico Express", "precio": 45000, "desc": 50, "horas": 4, "img": "https://images.unsplash.com/photo-1562577309-4932fdd64cd1?auto=format&fit=crop&w=500&q=60"},
            
            # Negocios
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Business Analytics", "precio": 1400000, "desc": 25, "img": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Emprendimiento Digital", "precio": 1000000, "desc": 10, "img": "https://images.unsplash.com/photo-1556761175-5973dc0f32d7?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "CARRERA", "titulo": "Finanzas Corporativas", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "RELAMPAGO", "titulo": "OKRs para Startups", "precio": 40000, "desc": 30, "horas": 3, "img": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?auto=format&fit=crop&w=500&q=60"},
            {"area": "Negocios", "tipo": "RELAMPAGO", "titulo": "Negociación Estratégica", "precio": 35000, "desc": 50, "horas": 2, "img": "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=500&q=60"},
            
            # Producto
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Product Management", "precio": 1500000, "desc": 30, "img": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Scrum Master", "precio": 1100000, "desc": 15, "img": "https://images.unsplash.com/photo-1531403009284-440f080d1e12?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "CARRERA", "titulo": "Agile Coach Bootcamp", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1517048676732-d65bc937f952?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "RELAMPAGO", "titulo": "Roadmapping Efectivo", "precio": 30000, "desc": 40, "horas": 2, "img": "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?auto=format&fit=crop&w=500&q=60"},
            {"area": "Producto", "tipo": "RELAMPAGO", "titulo": "User Research Express", "precio": 45000, "desc": 60, "horas": 4, "img": "https://images.unsplash.com/photo-1573164713988-8665fc963095?auto=format&fit=crop&w=500&q=60"},
            
            # Programación y Desarrollo
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Full Stack Web Bootcamp", "precio": 1900000, "desc": 70, "img": "https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Backend Developer con Python", "precio": 1400000, "desc": 30, "img": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "CARRERA", "titulo": "Mobile App Development", "precio": 1600000, "desc": 20, "img": "https://images.unsplash.com/photo-1551650975-87deedd944c3?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "RELAMPAGO", "titulo": "Git y GitHub Master", "precio": 20000, "desc": 50, "horas": 2, "img": "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?auto=format&fit=crop&w=500&q=60"},
            {"area": "Programación y Desarrollo", "tipo": "RELAMPAGO", "titulo": "Docker Express", "precio": 45000, "desc": 40, "horas": 4, "img": "https://images.unsplash.com/photo-1605379399642-870262d3d051?auto=format&fit=crop&w=500&q=60"},
        ]
        
        for c_data in cursos_data:
            kwargs = {
                "titulo": c_data["titulo"],
                "descripcion": "Descripción detallada del curso. Aprenderás herramientas clave demandadas en el mercado con profesores expertos.",
                "area": areas[c_data["area"]],
                "tipo": c_data["tipo"],
                "precio_original": c_data["precio"],
                "descuento_porcentaje": c_data["desc"],
                "cupos_totales": 50,
                "cupos_disponibles": 50,
                "imagen_url": c_data["img"]
            }
            if c_data["tipo"] == "CARRERA":
                kwargs["nivel"] = "Principiante a Avanzado"
                kwargs["semanas_duracion"] = 24
                kwargs["cantidad_cursos"] = 4
            else:
                kwargs["duracion_horas"] = c_data["horas"]
                
            Curso.objects.create(**kwargs)
            
        self.stdout.write(self.style.SUCCESS(f"¡Base de datos poblada con {Curso.objects.count()} cursos!"))
        self.stdout.write(self.style.SUCCESS("Usuario Admin: coordinador | Contraseña: admin123"))
'''
write_file('core/management/commands/seed_data.py', seed_script)
write_file('core/management/commands/__init__.py', '')
write_file('core/management/__init__.py', '')

# Remove admin from core/admin.py (user wants NO django-admin)
write_file('core/admin.py', '# Admin deshabilitado por requerimiento')

print("Files generated successfully.")
