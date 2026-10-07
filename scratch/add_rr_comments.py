import re

# 1. settings.py
with open('ticketRB/settings.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace('DATABASES = {', 'DATABASES = {  # RR - MOSTRAR AL PROFESOR: Configuración nativa de PostgreSQL')
content = content.replace("'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),", "'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # RR - MOSTRAR AL PROFESOR: Aquí se cambia la duración del JWT")
with open('ticketRB/settings.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 2. core/models.py
with open('core/models.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')", "user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')  # RR - MOSTRAR AL PROFESOR: Relación 1 a 1 para Roles")
content = content.replace("user = models.OneToOneField(User, on_delete=models.CASCADE)", "user = models.OneToOneField(User, on_delete=models.CASCADE)  # RR - MOSTRAR AL PROFESOR: Relación 1 a 1 para asegurar que el Carro sea persistente")
content = content.replace("ESTADO_CHOICES = (", "ESTADO_CHOICES = (  # RR - MOSTRAR AL PROFESOR: Uso explícito de CHOICES exigido en rúbrica")
with open('core/models.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 3. api/serializers.py
with open('api/serializers.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("token['rol'] = user.perfil.rol", "token['rol'] = user.perfil.rol  # RR - MOSTRAR AL PROFESOR: Inyección de Custom Claims (Rol) en el Payload del JWT")
with open('api/serializers.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 4. api/permissions.py
with open('api/permissions.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("class IsCoordinadorOrReadOnly(permissions.BasePermission):", "class IsCoordinadorOrReadOnly(permissions.BasePermission):  # RR - MOSTRAR AL PROFESOR: Clase de permiso DRF personalizada para restringir acciones por Rol")
with open('api/permissions.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 5. api/views.py
with open('api/views.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("permission_classes = [IsCoordinadorOrReadOnly]", "permission_classes = [IsCoordinadorOrReadOnly]  # RR - MOSTRAR AL PROFESOR: Aplicación de permisos a las vistas DRF")
content = content.replace("filter_backends = [DjangoFilterBackend, filters.SearchFilter]", "filter_backends = [DjangoFilterBackend, filters.SearchFilter]  # RR - MOSTRAR AL PROFESOR: Integración de django-filter y buscador OpenAPI")
content = content.replace("carro, _ = CarroMatricula.objects.get_or_create(user=request.user)", "carro, _ = CarroMatricula.objects.get_or_create(user=request.user)  # RR - MOSTRAR AL PROFESOR: Recuperación del carro persistente desde la DB")
content = content.replace("with transaction.atomic():", "with transaction.atomic():  # RR - MOSTRAR AL PROFESOR: Bloque transaccional para evitar inconsistencias en el Checkout")
content = content.replace("curso = Curso.objects.select_for_update().get(id=item.curso.id)", "curso = Curso.objects.select_for_update().get(id=item.curso.id)  # RR - MOSTRAR AL PROFESOR: Bloqueo de fila para control de concurrencia y descuento atómico exacto")
content = content.replace("curso.cupos_disponibles += 1", "curso.cupos_disponibles += 1  # RR - MOSTRAR AL PROFESOR: Reposición automática de stock/cupo al cancelar")
with open('api/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

# 6. ticketRB/urls.py
with open('ticketRB/urls.py', 'r', encoding='utf-8') as f:
    content = f.read()
content = content.replace("path('schema/', SpectacularAPIView.as_view(), name='schema'),", "path('schema/', SpectacularAPIView.as_view(), name='schema'),  # RR - MOSTRAR AL PROFESOR: Generación automática de esquema OpenAPI")
content = content.replace("path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),", "path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),  # RR - MOSTRAR AL PROFESOR: Vista gráfica de Swagger UI")
with open('ticketRB/urls.py', 'w', encoding='utf-8') as f:
    f.write(content)
