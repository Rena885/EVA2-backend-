from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.db import transaction
from django.shortcuts import get_object_or_404
from core.models import Curso, CarroMatricula, ItemCarro, Matricula, DetalleMatricula, Area
from .serializers import CursoSerializer, CarroMatriculaSerializer, ItemCarroSerializer
from .permissions import IsCoordinador, IsCoordinadorOrReadOnly


from .serializers import AreaSerializer
class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet de solo lectura para listar las áreas de conocimiento."""
    queryset = Area.objects.all()
    serializer_class = AreaSerializer

class CursoViewSet(viewsets.ModelViewSet):
    """ViewSet para exponer el CRUD de Cursos. Protegido por rol."""
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [IsCoordinadorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['area', 'precio_final']
    search_fields = ['titulo']

class CarroViewSet(viewsets.ViewSet):
    """ViewSet para consultar el Carro de Compras persistente del estudiante."""
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
    """
    Endpoint para procesar el pago. Usa atomic transactions y select_for_update
    para validar y descontar el stock en tiempo real evitando race conditions.
    """
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
                    raise ValueError(f'¡Atención! El curso "{curso.titulo}" que deseas en el carrito ya no está disponible debido a compras de otros clientes.')
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
    """Endpoint para cancelar una orden y reponer automáticamente los cupos."""
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

from .serializers import MatriculaSerializer
class MisMatriculasView(generics.ListAPIView):
    serializer_class = MatriculaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Matricula.objects.filter(user=self.request.user)
