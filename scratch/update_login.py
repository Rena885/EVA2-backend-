import os

content = open('core/views.py', 'r', encoding='utf-8').read()

new_logic = """def login_view(request):
    if request.GET.get('timeout') == '1':
        from django.contrib import messages
        messages.warning(request, 'Tu sesión ha expirado por tiempo de inactividad (3 minutos). Vuelve a iniciar sesión.')
        
    if request.user.is_authenticated:"""

import re
content = re.sub(r'def login_view\(request\):\s*if request\.user\.is_authenticated:', new_logic, content)

open('core/views.py', 'w', encoding='utf-8').write(content)
