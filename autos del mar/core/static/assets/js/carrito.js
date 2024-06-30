const carrito = () => {
    const idProducto = (document.getElementById('idProducto').textContent);

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
    console.log("se añadio el producto al carrito")
}

const btn = document.getElementById('btnPrueba')
btn.addEventListener('click', carrito)






