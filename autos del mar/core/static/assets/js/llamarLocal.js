// static/js/actualizar_carrito.js
export function enviarInfo() {
    // Obtener datos del localStorage
    const carritoCompra = JSON.parse(localStorage.getItem('carritoCompra'));

    // Enviar datos al backend de Django
    fetch("localHost:8000/carrito", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: carritoCompra,
    })
    .then(response => response.json())
    .then(data => {
        if (data.carritoCompra !== null) {
            data.map((producto) => {
                // Añadir producto al carrito de compras
                const { idProducto, cantidadProducto } = producto;
                // Construir HTML para cada producto y añadir al contenedor
                const productoHTML = `<div>${idProducto} - Cantidad: ${cantidadProducto}</div>`;
                contenedorProductos.innerHTML += productoHTML;
        });
        }
    })
    .catch(error => {
        console.error('Error al obtener datos del carrito:', error);
    });
}
