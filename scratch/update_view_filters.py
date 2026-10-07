import os

content = open('api/views.py', 'r', encoding='utf-8').read()
new_view = """class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsCoordinadorOrReadOnly]
    filterset_fields = ['area', 'precio_final']
    search_fields = ['titulo']"""

import re
content = re.sub(r'class CursoViewSet\(viewsets\.ModelViewSet\):.*?permission_classes = \[IsCoordinadorOrReadOnly\]', new_view, content, flags=re.DOTALL)
open('api/views.py', 'w', encoding='utf-8').write(content)
