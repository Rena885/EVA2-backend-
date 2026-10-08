import os
import re

# 1. settings.py
with open('ticketRB/settings.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR - PostgreSQL:.*?\"\"\"', '\"\"\"\\nRR - BD: ¿Qué es? Es la conexión física al motor local. Usamos django.db.backends.postgresql con credenciales.\\n\"\"\"', content, flags=re.DOTALL)
content = re.sub(r'# RR -JWT:.*', '# RR - JWT: ¿Qué es? JSON Web Token es una "pulsera" criptográfica para entrar a la API sin gastar RAM del servidor. Aquí se configura su vida (60 min).', content)
with open('ticketRB/settings.py', 'w', encoding='utf-8') as f: f.write(content)

# 2. core/models.py
with open('core/models.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR -Relaci.*?(?=user =)', '    \"\"\"\\n    RR - Relación 1:1: ¿Qué es? Es un vínculo exclusivo. Un Usuario nativo de Django solo puede tener un único PerfilUsuario.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -Carro Persistente.*?(?=user =)', '    \"\"\"\\n    RR - Carro Persistente: ¿Qué es? Es un carro que no vive en cookies temporales, sino en una tabla real de PostgreSQL atado 1 a 1 al Usuario.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -CHOICES.*?(?=ESTADO_CHOICES =)', '    \"\"\"\\n    RR - CHOICES: ¿Qué es? Es una regla estricta a nivel de Base de Datos. Evita que escriban estados inventados como "Patata", forzando a elegir opciones predefinidas.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
with open('core/models.py', 'w', encoding='utf-8') as f: f.write(content)

# 3. serializers.py
with open('api/serializers.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'# RR - JWT Custom Claim:.*', '# RR - Custom Claims: ¿Qué es? Es inyectar datos propios (como el ROL) dentro del Payload del JWT, para no re-consultar la DB.', content)
with open('api/serializers.py', 'w', encoding='utf-8') as f: f.write(content)

# 4. permissions.py
with open('api/permissions.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR -Permisos RBAC.*?(?=class IsCoordinadorOrReadOnly)', '\"\"\"\\nRR - Permisos (RBAC): ¿Qué es? Barrera de seguridad de DRF. Lee el token JWT y si no eres Coordinador, te prohíbe crear cursos.\\n\"\"\"\\n', content, flags=re.DOTALL)
with open('api/permissions.py', 'w', encoding='utf-8') as f: f.write(content)

# 5. views.py
with open('api/views.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR -Seguridad API.*?(?=permission_classes)', '    \"\"\"\\n    RR - Seguridad API: Protege este endpoint con la barrera IsCoordinadorOrReadOnly.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -Filtros API.*?(?=filter_backends)', '    \"\"\"\\n    RR - Filtros y Búsqueda: ¿Qué es? Permite buscar cursos por ID exacto (?area=1) o texto (?search=Java) sin descargar toda la DB.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -L.gica Carro.*?(?=carro, _ =)', '        \"\"\"\\n        RR - Lógica Carro Persistente: get_or_create consulta la BD. Así recupera los ítems si venían de ayer.\\n        \"\"\"\\n        ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -Transacci.n.*?(?=with transaction\.atomic)', '        \"\"\"\\n        RR - Ciclo Transaccional (.atomic): ¿Qué es? Regla del Todo o Nada. Si el pago o descuento falla, rebobina todo (Rollback).\\n        \"\"\"\\n        ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -Stock At.mico.*?(?=curso = Curso)', '                \"\"\"\\n                RR - Stock Atómico: ¿Qué es? Bloquea la fila en PostgreSQL. Si 2 compran el último cupo, frena a uno para evitar sobreventas.\\n                \"\"\"\\n                ', content, flags=re.DOTALL)
content = re.sub(r'\"\"\"\s*RR -Reposici.n Stock.*?(?=curso\.cupos_disponibles)', '                \"\"\"\\n                RR - Reposición: Si se cancela la orden, devuelve el cupo.\\n                \"\"\"\\n                ', content, flags=re.DOTALL)
with open('api/views.py', 'w', encoding='utf-8') as f: f.write(content)

# 6. urls.py
with open('api/urls.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR -OpenAPI.*?(?=path\(\'schema/\')', '    \"\"\"\\n    RR - Swagger OpenAPI: ¿Qué es? Estándar mundial para documentar APIs. Autogenera la interfaz visual /api/docs/ para testear.\\n    \"\"\"\\n    ', content, flags=re.DOTALL)
with open('api/urls.py', 'w', encoding='utf-8') as f: f.write(content)
