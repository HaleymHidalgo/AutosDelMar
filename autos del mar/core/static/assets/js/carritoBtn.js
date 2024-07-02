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
