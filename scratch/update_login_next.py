import os

with open('core/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_login = """def login_view(request):
    if request.GET.get('timeout') == '1':
        from django.contrib import messages
        messages.warning(request, 'Tu sesión ha expirado por tiempo de inactividad (3 minutos). Vuelve a iniciar sesión.')
        
    next_url = request.GET.get('next')
    
    if request.user.is_authenticated:
        if request.user.perfil.rol in ['COORDINADOR', 'ADMIN']:
            return redirect(next_url or 'panel')
        return redirect(next_url or 'catalogo')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.perfil.rol in ['COORDINADOR', 'ADMIN']:
                request.session.set_expiry(180)
                return redirect(next_url or 'panel')
            return redirect(next_url or 'catalogo')
    else:"""

import re
content = re.sub(r"def login_view\(request\):.*?else:", new_login, content, flags=re.DOTALL)

with open('core/views.py', 'w', encoding='utf-8') as f:
    f.write(content)
