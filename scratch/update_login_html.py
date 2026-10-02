import os

content = open('templates/auth/login.html', 'r', encoding='utf-8').read()
messages_block = """
                {% if messages %}
                    {% for message in messages %}
                        <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                            {{ message }}
                            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                        </div>
                    {% endfor %}
                {% endif %}
                """
content = content.replace('<form method="POST">', messages_block + '<form method="POST">')
open('templates/auth/login.html', 'w', encoding='utf-8').write(content)
