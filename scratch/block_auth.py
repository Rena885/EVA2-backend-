import os

with open('templates/curso_detalle.html', 'r', encoding='utf-8') as f:
    content = f.read()

blocked_content = """<div class="container mb-5">
    {% if not user.is_authenticated %}
    <div class="row justify-content-center">
        <div class="col-md-8 text-center py-5">
            <div class="card border-0 shadow-sm rounded-4 p-5 bg-light">
                <i class="bi bi-lock-fill display-1 text-muted mb-3"></i>
                <h3 class="fw-bold">Contenido Bloqueado</h3>
                <p class="lead text-muted">Para ver el contenido completo del curso y poder matricularte, primero tienes que registrarte o iniciar sesión.</p>
                <div class="mt-4">
                    <a href="{% url 'login' %}?next={{ request.path }}" class="btn btn-dark px-4 py-2 me-2 fw-bold">Iniciar Sesión</a>
                    <a href="{% url 'register' %}" class="btn btn-outline-dark px-4 py-2 fw-bold">Registrarme</a>
                </div>
            </div>
        </div>
    </div>
    {% else %}"""

content = content.replace('<div class="container mb-5">', blocked_content)
content = content.replace('{% endblock %}', '    {% endif %}\n</div>\n{% endblock %}')

with open('templates/curso_detalle.html', 'w', encoding='utf-8') as f:
    f.write(content)
