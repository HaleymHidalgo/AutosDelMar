document.addEventListener('DOMContentLoaded', () => {
    const boton_eliminar = document.getElementById('eliminarbtn');

    if (boton_eliminar) {
        boton_eliminar.addEventListener('click', () => {
            const id = boton_eliminar.getAttribute('data-vehiculo-id');
            eliminarVehiculo(id);
        });
    }

    function eliminarVehiculo(id) {
        fetch(`http://localhost:8000/vendedor/eliminarProducto/${id}`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',  // Asegúrate de que csrf_token esté definido correctamente en tu template
                'Content-Type': 'application/json'
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al eliminar vehículo');
            }
            return response.json();
        })
        .then(data => {
            console.log('Vehículo eliminado correctamente:', data);
            // Redirigir a la página de inicio después de eliminar
            window.location.href = "http://localhost:8000/vendedor/home.html";
        })
        .catch(error => {
            console.error('Error al eliminar vehículo:', error);
        });
    }
});