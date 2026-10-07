import os
import re

with open('templates/curso_detalle.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_buttons = """                    {% if ya_comprado %}
                        <div class="alert alert-success text-center mb-3 border-0 bg-success bg-opacity-10 text-success">
                            <i class="bi bi-check-circle-fill me-2"></i><strong>Ya posees este curso</strong>
                        </div>
                        <a href="{% url 'mis_cursos' %}" class="btn btn-success w-100 py-3 fw-bold">
                            Ir a Mis Cursos <i class="bi bi-play-circle-fill ms-1"></i>
                        </a>
                    {% elif curso.tipo == 'RELAMPAGO' or curso.cupos_disponibles > 0 %}"""

content = content.replace("{% if curso.tipo == 'RELAMPAGO' or curso.cupos_disponibles > 0 %}", new_buttons)

with open('templates/curso_detalle.html', 'w', encoding='utf-8') as f:
    f.write(content)
