document.addEventListener('DOMContentLoaded', () => {
    //Cancelo el evento de click del formualario
    event.preventDefault();
    // Obtener el token CSRF desde la meta etiqueta
    const csrfTokenMeta = document.querySelector('meta[name="csrf-token"]');
        if (!csrfTokenMeta) {
            console.error('CSRF token meta tag not found!');
            return;
        }
    const csrfToken = csrfTokenMeta.getAttribute('content');

    const boton_eliminar = document.getElementById('eliminarbtn');
    boton_eliminar.addEventListener('click', async() => {
        //obtenemos el id del vehículo a eliminar
        id = parseInt(document.getElementById('hiddenId').value)
        // Intentaremos enviar una petición para eliminar el vehículo
        try {
            const response = await fetch(`http://localhost:8000/vendedor/eliminarProducto/${id}`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            });
            //el metodo .ok devuelve un booleano que indica si la respuesta fue correcta (status 200-299)
            if (response.ok) {
                console.log("Producto eliminado correctamente");
                window.location.href = 'http://localhost:8000/vendedor/home'
            } else {
                // Manejar casos donde el servidor no responde con estado 204
                console.error(`Error al eliminar producto. Código de estado: ${response.status}`);
            }
        } catch (error) {
            console.error("Error de red:", error);
        }
    })
});