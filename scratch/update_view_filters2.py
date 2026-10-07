import os
import re

content = open('api/views.py', 'r', encoding='utf-8').read()

if 'from rest_framework import filters' not in content:
    content = 'from rest_framework import filters\nfrom django_filters.rest_framework import DjangoFilterBackend\n' + content

new_view = """class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsCoordinadorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'precio_final']
    search_fields = ['titulo']"""

content = re.sub(r'class CursoViewSet\(viewsets\.ModelViewSet\):.*?search_fields = \[\'titulo\'\]', new_view, content, flags=re.DOTALL)
open('api/views.py', 'w', encoding='utf-8').write(content)
