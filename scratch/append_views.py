import sys
content = open('core/views.py', 'r', encoding='utf-8').read()
new_views = """
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
            from core.models import PerfilUsuario
            PerfilUsuario.objects.create(user=user, rol='COORDINADOR')
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
"""
open('core/views.py', 'w', encoding='utf-8').write(content + new_views)
