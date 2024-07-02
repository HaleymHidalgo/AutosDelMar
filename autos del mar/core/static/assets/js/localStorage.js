//funcion guardar datos en local storage
const carrito = () => {
    const idProducto = parseInt(document.getElementById('idProducto').value);
    //const cantidadProducto = parseInt(document.getElementById('cantidadProducto').textContent);
    const cantidadProducto = 1;
    
    if(localStorage.getItem('carritoCompra') !== null){
        const carrito = JSON.parse(localStorage.getItem('carritoCompra'))
        const producto = {
            "idProducto":idProducto,
            "cantidadProducto": cantidadProducto
        }
    
        carrito.push(producto)
        localStorage.setItem('carritoCompra', JSON.stringify(carrito))
        }else{
        const producto = {
            "idProducto":idProducto,
            "cantidadProducto": cantidadProducto
        }
        localStorage.setItem('carritoCompra', JSON.stringify([producto]))
    }
}

const btn = document.getElementById('btnAniadir')
btn.addEventListener('click', carrito)



