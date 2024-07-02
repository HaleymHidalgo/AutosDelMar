// Script para validar el formulario antes de enviarlo
document.getElementById('registroformulario').addEventListener('submit', function(event) {
    let errorElement = document.getElementById('error');
    errorElement.textContent = '';  // Limpiar mensaje de error al inicio

    // Obtener valores de los campos
    let rutInput = document.getElementById('id_username');
    let rut = rutInput.value.trim();
    let password1 = document.getElementById('id_password1').value;
    let password2 = document.getElementById('id_password2').value;

    // Validación del RUT
    if (!validarRut(rut)) {
        mostrarError('El formato del RUT ingresado es inválido.');
        event.preventDefault();
        return false;
    }

    // Validación de las contraseñas
    if (password1 !== password2) {
        mostrarError('Las contraseñas no coinciden.');
        event.preventDefault();
        return false;
    }

    if (!validarContrasena(password1)) {
        mostrarError('La contraseña debe tener al menos 8 caracteres, incluir una letra mayúscula, una minúscula, y un número.');
        event.preventDefault();
        return false;
    }

    return true;  // Permitir enviar el formulario si todas las validaciones son exitosas
});

// Función para mostrar mensaje de error
function mostrarError(mensaje) {
    let errorElement = document.getElementById('error');
    errorElement.textContent = mensaje;
    errorElement.style.color = 'red';
}

// Función para validar el formato del RUT
function validarRut(rut) {
    return /^[0-9]{7,8}[-|‐]{1}[0-9kK]{1}$/.test(rut);
}

// Función para validar la complejidad de la contraseña
function validarContrasena(password) {
    let regex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$/;
    return regex.test(password);
}
