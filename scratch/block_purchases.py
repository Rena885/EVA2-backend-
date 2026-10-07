import os
import re

with open('api/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_perform_create = """def perform_create(self, serializer):
        carro, _ = CarroMatricula.objects.get_or_create(user=self.request.user)
        curso = serializer.validated_data['curso']
        if ItemCarro.objects.filter(carro=carro, curso=curso).exists():
            raise serializers.ValidationError({"detail": "Ya tienes el curso en el carrito."})
        if DetalleMatricula.objects.filter(matricula__user=self.request.user, matricula__estado='PAGADO', curso=curso).exists():
            raise serializers.ValidationError({"detail": "Ya has comprado este curso anteriormente."})
        serializer.save(carro=carro)"""

content = re.sub(r'def perform_create\(self, serializer\):.*?serializer\.save\(carro=carro\)', new_perform_create, content, flags=re.DOTALL)

checkout_validation = """if not items_carro.exists():
            return Response({"error": "El carro está vacío"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar si ya compró algún curso del carro
        for item in items_carro:
            if DetalleMatricula.objects.filter(matricula__user=request.user, matricula__estado='PAGADO', curso=item.curso).exists():
                raise ValueError(f"No puedes volver a comprar '{item.curso.titulo}' porque ya lo has pagado anteriormente.")"""

content = re.sub(r'if not items_carro.exists\(\):.*?status\.HTTP_400_BAD_REQUEST\)', checkout_validation, content, flags=re.DOTALL)

with open('api/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
