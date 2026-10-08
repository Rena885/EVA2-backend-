import os
import re

# 1. settings.py
with open('ticketRB/settings.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'\"\"\"\s*RR -PostgreSQL:.*?\"\"\"', '"""\nRR - BD: ¿Qué es? Es la conexión física al motor local. Usamos django.db.backends.postgresql con credenciales.\n"""', content, flags=re.DOTALL)
with open('ticketRB/settings.py', 'w', encoding='utf-8') as f: f.write(content)

# 2. core/models.py
with open('core/models.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'user = models\.OneToOneField\(User, on_delete=models\.CASCADE, related_name=\'perfil\'\).*', '"""\n    RR - Relación 1:1: ¿Qué es? Es un vínculo exclusivo. Un Usuario nativo de Django solo puede tener un único PerfilUsuario.\n    """\n    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name=\'perfil\')', content)
content = re.sub(r'user = models\.OneToOneField\(User, on_delete=models\.CASCADE\).*', '"""\n    RR - Carro Persistente: ¿Qué es? Es un carro que no vive en cookies temporales, sino en una tabla real de PostgreSQL atado 1 a 1 al Usuario.\n    """\n    user = models.OneToOneField(User, on_delete=models.CASCADE)', content)
content = re.sub(r'ESTADO_CHOICES = \(\s*(?!#)', '"""\n    RR - CHOICES: ¿Qué es? Es una regla estricta a nivel de Base de Datos. Evita que escriban estados inventados como "Patata", forzando a elegir opciones predefinidas.\n    """\n    ESTADO_CHOICES = (', content)
with open('core/models.py', 'w', encoding='utf-8') as f: f.write(content)

# 3. serializers.py
with open('api/serializers.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'token\[\'rol\'\] = user\.perfil\.rol.*', 'token[\'rol\'] = user.perfil.rol  # RR - Custom Claims: ¿Qué es? Es inyectar datos (como el ROL) dentro del Payload del JWT, para no re-consultar la DB.', content)
with open('api/serializers.py', 'w', encoding='utf-8') as f: f.write(content)

