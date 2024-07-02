const form = document.getElementById('formRegistro');
const nombre = document.getElementById('id_first_name');
const apellido = document.getElementById('id_last_name');
const rut = document.getElementById('id_username');
const email = document.getElementById('id_email');
const password = document.getElementById('id_password1');
const password2 = document.getElementById('id_password2');
const errorElement = document.getElementById('error-message'); // Elemento para mostrar mensajes de error generales

form.addEventListener('submit', function(e) {
    e.preventDefault();
    checkInputsRegistro();
});

function checkInputsRegistro() {
    const nombreValue = nombre.value.trim();
    const apellidoValue = apellido.value.trim();
    const rutValue = rut.value.trim();
    const emailValue = email.value.trim();
    const passwordValue = password.value.trim();
    const password2Value = password2.value.trim();
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

    if(rutValue === '') {
        setErrorFor(rut, 'Rut necesario');
        valid = false;
    } else if (!isRut(rutValue)){
        setErrorFor(rut, 'No ingresó un rut válido ej:(99.999.999-k)');
        valid = false;
    } else {
        setSuccessFor(rut);
    }

    if(emailValue === '') {
        setErrorFor(email, 'Email necesario');
        valid = false;
    } else if (!isEmail(emailValue)) {
        setErrorFor(email, 'No ingresó un email válido');
        valid = false;
    } else {
        setSuccessFor(email);
    }

    if(passwordValue === '') {
        setErrorFor(password, 'Necesita una contraseña');
        valid = false;
    } else {
        setSuccessFor(password);
    }

    if(password2Value === '') {
        setErrorFor(password2, 'Debe reingresar la contraseña');
        valid = false;
    } else if(passwordValue !== password2Value) {
        setErrorFor(password2, 'Las contraseñas no coinciden');
        valid = false;
    } else {
        setSuccessFor(password2);
    }

    // Si todas las validaciones son exitosas, puedes enviar el formulario
    if (valid) {
        form.submit();
    }
}

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    const small = formControl.querySelector('small');
    formControl.className = 'form-control error';
    small.innerText = message;
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function isEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}

function isRut(rut) {
    return /^(\d{1,2}(?:[\.]?\d{3}){2}-[\dkK])$/.test(rut);
}
