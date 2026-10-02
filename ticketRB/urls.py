
from django.urls import path, include
from django.shortcuts import render
from core import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    # API
    path('api/', include('api.urls')),
    
    # Vistas UI
    path('', views.home, name='home'),
    path('recursos/', views.recursos_view, name='recursos'),
    path('metodologia/', views.metodologia_view, name='metodologia'),
    path('cursos/', views.catalogo, name='catalogo'),
    path('cursos/<int:pk>/', views.curso_detalle, name='curso_detalle'),
    path('carro/', views.carro_view, name='carro'),
    path('mis-cursos/', views.mis_cursos, name='mis_cursos'),
    path('404/', lambda request: render(request, '404.html'), name='404_preview'),
    
    # Auth
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    
    # Panel Admin
    path('panel/', views.panel_view, name='panel'),
    path('panel/curso/nuevo/', views.panel_curso_crear, name='panel_curso_crear'),
    path('panel/curso/<int:pk>/editar/', views.panel_curso_editar, name='panel_curso_editar'),
    path('panel/curso/<int:pk>/eliminar/', views.panel_curso_eliminar, name='panel_curso_eliminar'),
    path('panel/usuarios/', views.panel_usuarios, name='panel_usuarios'),
]

handler404 = 'core.views.error_404'

from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]
