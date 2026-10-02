import os

content = """{% extends 'base.html' %}
{% block title %}Usuarios Registrados - ticketRB{% endblock %}
{% block content %}
<div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-5">
        <div>
            <h2 class="fw-bold m-0" style="color: var(--primary);">Usuarios Registrados</h2>
            <p class="text-muted mb-0">Listado de cuentas</p>
        </div>
        <div>
            <a href="{% url 'panel' %}" class="btn btn-outline-dark">Volver al Panel</a>
        </div>
    </div>

    <div class="card border-0 shadow-sm rounded-4 overflow-hidden">
        <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                    <tr>
                        <th class="py-3 px-4">ID</th>
                        <th class="py-3">USUARIO</th>
                        <th class="py-3">EMAIL</th>
                        <th class="py-3">ROL (PERFIL)</th>
                        <th class="py-3 px-4">FECHA DE REGISTRO</th>
                    </tr>
                </thead>
                <tbody>
                    {% for usuario in usuarios %}
                    <tr>
                        <td class="px-4 text-muted">#{{ usuario.id }}</td>
                        <td class="fw-medium">{{ usuario.username }}</td>
                        <td class="text-muted">{% if usuario.email %}{{ usuario.email }}{% else %}<em class="text-black-50">Sin email</em>{% endif %}</td>
                        <td>
                            {% if usuario.perfil.rol == 'COORDINADOR' %}
                                <span class="badge bg-primary text-white rounded-pill px-3">Coordinador</span>
                            {% elif usuario.perfil.rol == 'ADMIN' %}
                                <span class="badge bg-danger text-white rounded-pill px-3">Administrador</span>
                            {% else %}
                                <span class="badge bg-success text-white rounded-pill px-3">Estudiante</span>
                            {% endif %}
                        </td>
                        <td class="px-4 text-muted small">{{ usuario.date_joined|date:"d M Y, H:i" }}</td>
                    </tr>
                    {% empty %}
                    <tr>
                        <td colspan="5" class="text-center py-5 text-muted">No hay usuarios registrados.</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</div>
{% endblock %}"""

with open('templates/panel/usuarios.html', 'w', encoding='utf-8') as f:
    f.write(content)
