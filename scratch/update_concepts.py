import os
import re

files = {
    'ticketRB/settings.py': [
        (r'RR - PostgreSQL: Conexin nativa\.\s*Usamos motor postgresql\s*y pasamos credenciales \(usuario/pass\)\.',
         'RR - DB: ¿Qué es? Es la conexión física al motor. Usamos django.db.backends.postgresql con credenciales locales.'),
        (r'# RR -JWT: Usamos SimpleJWT\.\s*Aqu se configura la vida del\s*# Access Token \(60 min\)\.',
         '# RR - JWT: ¿Qué es? JSON Web Token es una "pulsera" criptográfica para entrar a la API sin gastar RAM del servidor. Aquí se configura su vida (60 min).')
    ],
    'core/models.py': [
        (r'RR - Carro Persistente: Relacin 1:1\.\s*Se guarda\s*fsicamente en PostgreSQL, por eso no se borra al\s*cerrar sesin\.',
         'RR - Carro Persistente: ¿Qué es? Es un carro que no vive en cookies temporales, sino en una tabla real de PostgreSQL atado 1 a 1 al Usuario. Si cambia de PC, el carro sigue ahí.'),
        (r'RR - CHOICES: Restringe el campo a una lista fija\s*\(ej\. PAGADO\)\.\s*Da integridad a la BD y evita estados\s*invlidos\.',
         'RR - CHOICES: ¿Qué es? Es una regla estricta a nivel de Base de Datos. Evita que escriban estados inventados como "Patata", forzando a elegir solo opciones predefinidas.'),
        (r'RR - Relacin 1:1: Vincula el User nativo de Django\s*con nuestro Perfil \(para asignarle un Rol\)\.',
         'RR - Relación 1:1: ¿Qué es? Es un vínculo exclusivo. Un Usuario nativo de Django solo puede tener un único PerfilUsuario (para manejar roles).')
    ],
    'api/serializers.py': [
        (r'# RR - JWT Custom Claim: Sobrescribimos get_token\s*# para inyectar el ROL en el token\.',
         '# RR - Custom Claims: ¿Qué es? Es inyectar datos propios (como el ROL) dentro del Payload del JWT, para que el Frontend sepa quién eres sin re-consultar la DB.')
    ],
    'api/permissions.py': [
        (r'RR - Permisos RBAC: Creamos permisos DRF\s*personalizados\.\s*Bloquea peticiones destructivas si el\s*JWT no tiene rol COORDINADOR\.',
         'RR - Permisos (RBAC): ¿Qué es? Barrera de seguridad de DRF. Lee el token JWT y si no eres Coordinador, te prohíbe borrar o crear cursos (Solo te deja hacer GET).')
    ],
    'api/views.py': [
        (r'RR -Seguridad API: Protege la vista aplicando nuestro\s*permiso IsCoordinadorOrReadOnly\.',
         'RR - Seguridad API: Protege este endpoint con la barrera IsCoordinadorOrReadOnly.'),
        (r'RR - Filtros API: django-filter habilita bsqueda\s*exacta por rea y motor de texto por ttulo\.',
         'RR - Filtros y Búsqueda: ¿Qué es? Permite buscar cursos por ID exacto (?area=1) o tipear texto parcial (?search=Java) sin descargar toda la DB de golpe.'),
        (r'RR - Transaccin: transaction\.atomic\(\) agrupa todo\.\s*Si algo falla \(ej\. sin stock\), hace rollback total\.',
         'RR - Ciclo Transaccional (.atomic): ¿Qué es? Es la regla del Todo o Nada. Si el pago o descuento falla a la mitad, rebobina todo (Rollback) para no dejar pagos a medias ni datos corruptos.'),
        (r'RR - Stock Atmico: select_for_update\(\) bloquea la\s*fila\.\s*Evita sobrecupos si 2 alumnos compran al mismo\s*milisegundo\.',
         'RR - Stock Atómico (Control Concurrencia): ¿Qué es? Bloquea temporalmente la fila en PostgreSQL. Si 2 alumnos compran el último cupo en el mismo milisegundo, frena a uno para evitar sobreventas.'),
        (r'RR - Lgica Carro: get_or_create consulta la DB\.\s*Si\s*el usuario ya tena tems de una sesin previa, los\s*recupera intactos\.',
         'RR - Lógica Carro Persistente: get_or_create consulta la BD en vez de crear uno vacío. Así, recupera los ítems si venían de ayer.')
    ],
    'api/urls.py': [
        (r'RR - OpenAPI: drf-spectacular lee modelos y\s*serializadores para autogenerar el esquema estndar\.',
         'RR - Swagger OpenAPI: ¿Qué es? Es el estándar mundial para documentar APIs. drf-spectacular lee nuestro código y autogenera la interfaz visual /api/docs/ para testear los botones.')
    ]
}

# The regexes above use \s* to match any spaces/newlines since the text is currently wrapped.
for filepath, replacements in files.items():
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old_regex, new_text in replacements:
        # We need to wrap the new_text nicely if it's going inside a docstring
        import textwrap
        wrapped = textwrap.fill(new_text, width=65)
        # If the original was a docstring, we replace the inside content.
        # It's easier to just do a search and replace over the known string parts, ignoring whitespace
        # But to be safe, I'll just write a cleaner script to inject the new text manually if regex is too messy.
