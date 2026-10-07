import os

with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_js = """                      if (response.ok) {
                          showToast('Curso agregado al carrito', 'success');
                          
                          // Fetch new cart count
                          const cartRes = await fetch(`/api/carro/`);
                          if (cartRes.ok) {
                              const cartData = await cartRes.json();
                              updateCartCounter(cartData.items.length);
                          }
                      } else if (response.status === 400) {
                          showToast('Ya tienes el curso en el carrito', 'warning');
                      } else {
                          showToast('Error al agregar al carrito', 'error');
                      }
                  } catch (error) {
                      showToast('Ya tienes el curso en el carrito', 'warning');
                  } finally {"""

new_js = """                      if (response.ok) {
                          showToast('Curso agregado al carrito', 'success');
                          
                          // Fetch new cart count
                          const cartRes = await fetch(`/api/carro/`);
                          if (cartRes.ok) {
                              const cartData = await cartRes.json();
                              updateCartCounter(cartData.items.length);
                          }
                      } else if (response.status === 400) {
                          let msg = data.detail ? (Array.isArray(data.detail) ? data.detail[0] : data.detail) : (data.non_field_errors ? data.non_field_errors[0] : 'Ya tienes el curso en el carrito');
                          showToast(msg, 'warning');
                      } else {
                          showToast('Error al agregar al carrito', 'error');
                      }
                  } catch (error) {
                      showToast('Error de conexión', 'error');
                  } finally {"""

content = content.replace(old_js, new_js)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)
