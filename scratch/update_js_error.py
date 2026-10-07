import os
import re

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_js = """                      if (response.ok) {
                          showToast('Curso agregado al carrito', 'success');
                          
                          // Fetch new cart count
                          const cartRes = await fetch(`/api/carro/`);
                          if (cartRes.ok) {
                              const cartData = await cartRes.json();
                              updateCartCounter(cartData.items.length);
                          }
                      } else if (response.status === 400) {
                          let msg = data.detail ? (Array.isArray(data.detail) ? data.detail[0] : data.detail) : 'Ya tienes el curso en el carrito';
                          showToast(msg, 'warning');
                      } else {
                          showToast('Error al agregar al carrito', 'error');
                      }
                  } catch (error) {
                      showToast('Error de conexión', 'error');
                  } finally {"""

content = re.sub(r"                      if \(response\.ok\).*?\} finally \{", new_js, content, flags=re.DOTALL)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
