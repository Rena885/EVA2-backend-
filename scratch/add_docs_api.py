import os

with open('api/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('class CursoViewSet(viewsets.ModelViewSet):', 'class CursoViewSet(viewsets.ModelViewSet):\n    """ViewSet para exponer el CRUD de Cursos. Protegido por rol."""')
content = content.replace('class AreaViewSet(viewsets.ReadOnlyModelViewSet):', 'class AreaViewSet(viewsets.ReadOnlyModelViewSet):\n    """ViewSet de solo lectura para listar las áreas de conocimiento."""')
content = content.replace('class CarroViewSet(viewsets.ViewSet):', 'class CarroViewSet(viewsets.ViewSet):\n    """ViewSet para consultar el Carro de Compras persistente del estudiante."""')
content = content.replace('class ItemCarroView(views.APIView):', 'class ItemCarroView(views.APIView):\n    """APIView para agregar ítems al carro asegurando que no se dupliquen."""')
content = content.replace('class ItemCarroDetailView(views.APIView):', 'class ItemCarroDetailView(views.APIView):\n    """APIView para eliminar ítems específicos del carro."""')
content = content.replace('def checkout(request):', 'def checkout(request):\n    """\n    Endpoint para procesar el pago. Usa atomic transactions y select_for_update\n    para validar y descontar el stock en tiempo real evitando race conditions.\n    """')
content = content.replace('def cancelar_matricula(request, pk):', 'def cancelar_matricula(request, pk):\n    """Endpoint para cancelar una orden y reponer automáticamente los cupos."""')

with open('api/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
