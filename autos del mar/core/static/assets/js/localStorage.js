//funcion guardar datos en local storage
const carrito = () => {
    const idProducto = parseInt(document.getElementById('idProducto').textContent);

    if(localStorage.getItem('carritoCompra') !== null){
        const carrito = JSON.parse(localStorage.getItem('carritoCompra'))
        const producto = {
            "idProducto":idProducto,
            "cantidadProducto": 1 
        }
    
        carrito.push(producto)
        localStorage.setItem('carritoCompra', JSON.stringify(carrito))
        }else{
        const producto = {
            "idProducto":idProducto,
            "cantidadProducto": 1
        }
        localStorage.setItem('carritoCompra', JSON.stringify([producto]))
    }
}

const btn = document.getElementById('btnAniadir')
btn.addEventListener('click', carrito)



