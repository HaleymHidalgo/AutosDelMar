const form = document.getElementById('formAcceso');
const rut = document.getElementById('id_usuario_id');
const password = document.getElementById('id_password');

form.addEventListener('submit', function(e) {
    e.preventDefault();
    checkInputsAcceso();
});

function checkInputsAcceso() {

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

function isRut(rut) {
    return /^(\d{1,2}\d{3}\d{3}-[\dkK])$/.test(rut);
}