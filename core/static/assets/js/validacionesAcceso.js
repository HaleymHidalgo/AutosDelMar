const form = document.getElementById('formAcceso');
const rut = document.getElementById('id_usuario_id');
const password = document.getElementById('id_password');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    checkInputsRegistro();
});

function checkInputsRegistro() {

    const rutValue = rut.value.trim();
    const passwordValue = password.value.trim();
    let valid = true;

    if(rutValue === '') {
        setErrorFor(rut, 'Rut necesario');
        valid = false;
    } else if (!isRut(rutValue)){
        setErrorFor(rut, 'No ingresó un rut válido');
        valid = false;
    } else {
        setSuccessFor(rut);
    }

    if(passwordValue === '') {
        setErrorFor(password, 'Necesita una contraseña');
        valid = false;
    } else {
        setSuccessFor(password);
    }

    // Si todas las validaciones son exitosas, puedes enviar el formulario
    if (valid) {
        form.submit();
    }
}

function setErrorFor(input, message) {
    const formControl = input.parentElement;
    formControl.className = 'form-control error';
	const errorMessage = document.getElementById('errorAcceso');
	errorMessage.innerText = message;
}

function setSuccessFor(input) {
    const formControl = input.parentElement;
    formControl.className = 'form-control success';
}

function isEmail(email) {
    return /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(email);
}

function isRut(rut) {
    return /^(\d{1,2}\d{3}\d{3}-[\dkK])$/.test(rut);
}