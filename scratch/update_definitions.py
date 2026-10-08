import os
import re

files = {
    'ticketRB/settings.py': [
        (r'\"\"\"\n\s*RR - PostgreSQL:.*?\"\"\"', '\"\"\"\\nRR - DB: ¿Qué es? Es la conexión física al motor. Usamos django.db.backends.postgresql con credenciales locales.\\n\"\"\"'),
        (r'# RR -JWT:.*?\(60 min\)\.', '# RR - JWT: ¿Qué es? JSON Web Token es una "pulsera" criptográfica para entrar a la API sin gastar RAM del servidor. Aquí se configura su vida (60 min).')
    ],
    'core/models.py': [
        (r'\"\"\"\n\s*RR - Carro Persistente:.*?\"\"\"', '\"\"\"\\n    RR - Carro Persistente: ¿Qué es? Es un carro que no vive en cookies temporales, sino en una tabla real de PostgreSQL atado 1 a 1 al Usuario. Si cambia de PC, el carro sigue ahí.\\n    \"\"\"'),
        (r'\"\"\"\n\s*RR - CHOICES:.*?\"\"\"', '\"\"\"\\n    RR - CHOICES: ¿Qué es? Es una regla estricta a nivel de Base de Datos. Evita que escriban estados inventados como "Patata", forzando a elegir solo opciones predefinidas.\\n    \"\"\"'),
        (r'\"\"\"\n\s*RR - Relación 1:1:.*?\"\"\"', '\"\"\"\\n    RR - Relación 1:1: ¿Qué es? Es un vínculo exclusivo. Un Usuario nativo de Django solo puede tener un único PerfilUsuario (para manejar roles).\\n    \"\"\"')
    ],
    'api/serializers.py': [
        (r'# RR - JWT Custom Claim:.*', '# RR - Custom Claims: ¿Qué es? Es inyectar datos propios (como el ROL) dentro del Payload del JWT, para que el Frontend sepa quién eres sin re-consultar la DB.')
    ],
    'api/permissions.py': [
        (r'\"\"\"\n\s*RR - Permisos RBAC:.*?\"\"\"', '\"\"\"\\n    RR - Permisos (RBAC): ¿Qué es? Barrera de seguridad de DRF. Lee el token JWT y si no eres Coordinador, te prohíbe borrar o crear cursos (Solo te deja hacer GET).\\n    \"\"\"')
    ],
    'api/views.py': [
        (r'\"\"\"\n\s*RR - Seguridad API:.*?\"\"\"', '\"\"\"\\n    RR - Seguridad API: Protege este endpoint con la barrera IsCoordinadorOrReadOnly.\\n    \"\"\"'),
        (r'\"\"\"\n\s*RR - Filtros API:.*?\"\"\"', '\"\"\"\\n    RR - Filtros y Búsqueda: ¿Qué es? Permite buscar cursos por ID exacto (?area=1) o tipear texto parcial (?search=Java) sin descargar toda la DB de golpe.\\n    \"\"\"'),
        (r'\"\"\"\n\s*RR - Transacción:.*?\"\"\"', '\"\"\"\\n        RR - Ciclo Transaccional (.atomic): ¿Qué es? Es la regla del Todo o Nada. Si el pago o descuento falla a la mitad, rebobina todo (Rollback) para no dejar pagos a medias ni datos corruptos.\\n        \"\"\"'),
        (r'\"\"\"\n\s*RR - Stock Atómico:.*?\"\"\"', '\"\"\"\\n                RR - Stock Atómico (Control Concurrencia): ¿Qué es? Bloquea temporalmente la fila en PostgreSQL. Si 2 alumnos compran el último cupo en el mismo milisegundo, frena a uno para evitar sobreventas.\\n                \"\"\"'),
        (r'\"\"\"\n\s*RR - Lógica Carro:.*?\"\"\"', '\"\"\"\\n        RR - Lógica Carro Persistente: get_or_create consulta la BD en vez de crear uno vacío. Así, recupera los ítems si venían de ayer.\\n        \"\"\"')
    ],
    'api/urls.py': [
        (r'\"\"\"\n\s*RR - OpenAPI:.*?\"\"\"', '\"\"\"\\n    RR - Swagger OpenAPI: ¿Qué es? Es el estándar mundial para documentar APIs. drf-spectacular lee nuestro código y autogenera la interfaz visual /api/docs/ para testear los botones.\\n    \"\"\"')
    ]
}

for filepath, replacements in files.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_regex, new_text in replacements:
        content = re.sub(old_regex, new_text, content, flags=re.DOTALL)
        
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
