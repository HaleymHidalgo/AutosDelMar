

//Patrones de Formateo
validarRUT = (rut) => {
    // Expresión regular para validar el RUT
    const pattern = /^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$/;
    return pattern.test(rut);
}

validarPassword = (password) => {
    // Expresión regular para validar la contraseña
    const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    return pattern.test(password);
}

let formulario = document.getElementById('formulario_id')

formulario.addEventListener('submit', async (e) => {
    // Evita que se envíe el formulario
    e.preventDefault();

    // Obtenemos los valores del formulario
    let formObject = new FormData(formulario);
    let data = {};
    formObject.forEach((value, key) => {
        data[key] = value;
    });

    let rut = data.usuario_id;
    let password = data.password;

    // Validamos los campos del formulario
    if (rut == "" || password == "") {
        // Alerta campos vacíos
        swal({
            title: "Completa los campos",
            icon: "warning"
        });
    } else if (!validarRUT(rut) || !validarPassword(password)) {
        // Alerta datos inválidos
        swal({
            title: "Datos Invalidos",
            icon: "warning"
        });
    } else {
        try {
            console.log(object);
            let response = await fetch('/acceso_usuario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')  // Si estás usando CSRF en Django
                },
                body: JSON.stringify(data)
            });

            console.log(response);
            let responseData = await response.json();

            if (response.ok && responseData.ok) {
                swal({
                    title: "Acceso Correcto",
                    icon: "success"
                });
            } else {
                swal({
                    title: "Acceso Incorrecto",
                    icon: "error"
                });
            }
        } catch (error) {
            swal({
                title: "Error de conexión",
                icon: "error"
            });
        }
    }
});

// Función para obtener la cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


//window.location.href = "http://localhost:8000/inicio"
