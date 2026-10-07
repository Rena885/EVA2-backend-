import os

with open('templates/auth/login.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<form method="POST">', '<form method="POST" action="{% if request.GET.next %}?next={{ request.GET.next }}{% endif %}">')

with open('templates/auth/login.html', 'w', encoding='utf-8') as f:
    f.write(content)
