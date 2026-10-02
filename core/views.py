
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Curso, Area, Matricula, DetalleMatricula
from .forms import CursoForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def recursos_view(request):
    return render(request, 'recursos.html')

def metodologia_view(request):
    return render(request, 'metodologia.html')

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

def curso_detalle(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    # Recomendaciones: otros cursos de la misma área
    relacionados = Curso.objects.filter(area=curso.area).exclude(pk=curso.pk)[:3]
    return render(request, 'curso_detalle.html', {'curso': curso, 'relacionados': relacionados})

@login_required
def carro_view(request):
    return render(request, 'carro.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.perfil.rol in ['COORDINADOR', 'ADMIN']:
            return redirect('panel')
        return redirect('catalogo')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.perfil.rol in ['COORDINADOR', 'ADMIN']:
                # Cierre de sesión por inactividad de 3 minutos
                request.session.set_expiry(180)
                return redirect('panel')
            return redirect('catalogo')
    else:
        form = AuthenticationForm()
        
    form.fields['username'].label = "Nombre de usuario"
    form.fields['username'].widget.attrs.update({'placeholder': 'tu_usuario', 'autofocus': True})
        
    return render(request, 'auth/login.html', {'form': form})

def register_view(request):
    from .forms import RegistroUsuarioForm
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            # El perfil se crea automáticamente a través de las señales (core/signals.py)
            login(request, user)
            return redirect('catalogo')
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'auth/register.html', {'form': form})

# PANEL DE COORDINADOR
@login_required
def panel_view(request):
    if request.user.perfil.rol not in ['COORDINADOR', 'ADMIN']:
        return redirect('home')
        
    cursos = Curso.objects.all()
    matriculas = Matricula.objects.all().order_by('-fecha')
    
    return render(request, 'panel/dashboard.html', {
        'cursos': cursos,
        'matriculas': matriculas
    })

@login_required
def panel_curso_crear(request):
    if request.user.perfil.rol not in ['COORDINADOR', 'ADMIN']:
        return redirect('home')
        
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso creado con éxito.')
            return redirect('panel')
    else:
        form = CursoForm()
    return render(request, 'panel/curso_form.html', {'form': form, 'title': 'Crear Curso'})

@login_required
def panel_curso_editar(request, pk):
    if request.user.perfil.rol not in ['COORDINADOR', 'ADMIN']:
        return redirect('home')
        
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso actualizado con éxito.')
            return redirect('panel')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'panel/curso_form.html', {'form': form, 'title': 'Editar Curso'})

@login_required
def panel_curso_eliminar(request, pk):
    if request.user.perfil.rol not in ['COORDINADOR', 'ADMIN']:
        return redirect('home')
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        messages.success(request, 'Curso eliminado.')
        return redirect('panel')
    return render(request, 'panel/curso_confirm_delete.html', {'curso': curso})

from django.contrib.auth.models import User

@login_required
def mis_cursos(request):
    # Obtener todas las matrículas pagadas del usuario
    matriculas = Matricula.objects.filter(user=request.user, estado='PAGADO').order_by('-fecha').prefetch_related('detalles__curso')
    return render(request, 'mis_cursos.html', {'matriculas': matriculas})

@login_required
def panel_usuarios(request):
    if request.user.perfil.rol not in ['COORDINADOR', 'ADMIN']:
        return redirect('home')
        
    usuarios = User.objects.select_related('perfil').all().order_by('-date_joined')
    return render(request, 'panel/usuarios.html', {'usuarios': usuarios})

def error_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def panel_coordinadores(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('home')
    from core.models import PerfilUsuario
    coordinadores = PerfilUsuario.objects.filter(rol='COORDINADOR')
    return render(request, 'panel/coordinadores.html', {'coordinadores': coordinadores})

@login_required
def crear_coordinador(request):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = user.username
            user.save()
            user.perfil.rol = 'COORDINADOR'
            user.perfil.save()
            messages.success(request, 'Coordinador creado correctamente.')
            return redirect('panel_coordinadores')
    else:
        form = UserCreationForm()
        form.fields['username'].label = 'Correo Electrónico'
        form.fields['username'].widget.attrs.update({'type': 'email'})
    return render(request, 'panel/crear_coordinador.html', {'form': form})

@login_required
def eliminar_coordinador(request, pk):
    if request.user.perfil.rol != 'ADMIN':
        return redirect('home')
    from django.contrib.auth.models import User
    coordinador = get_object_or_404(User, pk=pk)
    if hasattr(coordinador, 'perfil') and coordinador.perfil.rol == 'COORDINADOR':
        coordinador.delete()
        messages.success(request, 'Coordinador eliminado correctamente.')
    return redirect('panel_coordinadores')
