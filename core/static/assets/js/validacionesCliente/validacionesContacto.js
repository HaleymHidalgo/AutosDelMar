const form = document.getElementById('formContacto');
const nombre = document.getElementById('id_nombre');
const apellido = document.getElementById('id_apellido');
const telefono = document.getElementById('id_telefono');
const correo = document.getElementById('id_correo');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    checkInputsContacto();
});

function checkInputsContacto() {

    const nombreValue = nombre.value.trim();
    const apellidoValue = apellido.value.trim();
    const telefonoValue = telefono.value.trim();
    const correoValue = correo.value.trim();
    let valid = true;

    if(nombreValue === '') {
        setErrorFor(nombre, 'Nombre necesario');
        valid = false;
    } else {
        setSuccessFor(nombre);
    }

    if(apellidoValue === '') {
        setErrorFor(apellido, 'Apellido necesario');
        valid = false;
    } else {
        setSuccessFor(apellido);
    }

    if(telefonoValue === '') {
        setErrorFor(telefono, 'Telefono necesario');
        valid = false;
    } else {
        setSuccessFor(telefono);
    }
    
    if(correoValue === '') {
        setErrorFor(correo, 'Email necesario');
        valid = false;
    } else if (!isEmail(correoValue)) {
        setErrorFor(correo, 'No ingresó un email válido');
        valid = false;
    } else {
        setSuccessFor(correo);
    }

    // Si todas las validaciones son exitosas, puedes enviar el formulario
    if (valid) {
        form.submit();
    }
}

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
	const errorMessage = document.getElementById('errorContacto');
	errorMessage.innerText = message;
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function isEmail(correo) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(correo);
}
