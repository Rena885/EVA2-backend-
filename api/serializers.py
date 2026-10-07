
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
    imagen_url = serializers.CharField(source='get_image', read_only=True)
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

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        fields = '__all__'
