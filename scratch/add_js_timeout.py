import os

content = open('templates/base.html', 'r', encoding='utf-8').read()

js_snippet = """
    {% if user.is_authenticated %}
        {% if user.perfil.rol == 'COORDINADOR' or user.perfil.rol == 'ADMIN' %}
        <script>
            // Cierre de sesión por inactividad de 3 minutos en el cliente
            let inactivityTime = function () {
                let time;
                window.onload = resetTimer;
                
                function logout() {
                    window.location.href = "{% url 'login' %}?timeout=1";
                }

                function resetTimer() {
                    clearTimeout(time);
                    time = setTimeout(logout, 180000); // 3 minutos
                }
            };
            inactivityTime();
        </script>
        {% endif %}
    {% endif %}
</body>"""

content = content.replace('</body>', js_snippet)
open('templates/base.html', 'w', encoding='utf-8').write(content)
