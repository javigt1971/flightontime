const modal = document.querySelector('#EquipoDialog');
const llamarModal = document.querySelector('#equipo');
const cerrarModal = document.querySelector('#btn-close');

const resultado = document.querySelector('#resultado');
const consultar = document.querySelector('#btn-action')


llamarAddEventListeners();
function llamarAddEventListeners() {
    llamarModal.addEventListener('click', () => {
        modal.showModal()
    });
    cerrarModal.addEventListener('click', () => {
        modal.close();
    });
}

function limpiarHTML() {
    while (resultado.firstChild) {
        resultado.removeChild(contenedor.firstChild);
    }
}
