
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from . import views

router = DefaultRouter()
router.register(r'cursos', views.CursoViewSet)
router.register(r'areas', views.AreaViewSet)

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
    
    # Mis Matriculas
    path('mis-matriculas/', views.MisMatriculasView.as_view(), name='mis-matriculas'),
    
    # Docs
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
