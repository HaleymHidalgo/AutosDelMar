//funcion limpiar carrito 
const btnLimpiar = document.getElementById('btnLimpiar');
btnLimpiar.addEventListener('click', () => {
    localStorage.removeItem('carritoCompra');
});

//funcion eliminar producto
const btnEliminarList = document.querySelectorAll('.btnEliminar');

    btnEliminarList.forEach(btnEliminar => {

        btnEliminar.addEventListener('click', () => {

            const idProducto = btnEliminar.getAttribute('data-producto-id');

            let carritoLocal = JSON.parse(localStorage.getItem('carritoCompra'));

            console.log(carritoLocal);

            const nuevoCarrito = carritoLocal.filter(producto => producto.idProducto !== idProducto);
            
            console.log(nuevoCarrito);
    })
});


// Función para mostrar los productos del localStorage en el carrito
const mostrarProductosCarrito = () => {
    const carrito = JSON.parse(localStorage.getItem('carritoCompra'));

    carrito.forEach(producto => {
        
    });
};

// Llama a esta función cuando se cargue la página para mostrar los productos del localStorage
mostrarProductosCarrito();
