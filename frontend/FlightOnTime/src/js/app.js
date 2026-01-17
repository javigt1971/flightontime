const modal = document.querySelector('#EquipoDialog');
const llamarModal = document.querySelector('#equipo');
const cerrarModal = document.querySelector('#btn-close');


llamarAddEventListeners();
function llamarAddEventListeners() {
    llamarModal.addEventListener('click', () => {
        modal.showModal()
    });
    cerrarModal.addEventListener('click', () => {
        modal.close();
    });
}