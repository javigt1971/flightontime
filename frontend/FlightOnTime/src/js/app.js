const modal = document.querySelector('#EquipoDialog');
const llamarModal = document.querySelector('#equipo');
const cerrarModal = document.querySelector('#btn-close');

const resultado = document.querySelector('#resultado');
const consultar = document.querySelector('#btn-action');

const formulario = document.querySelector('#formulario-vuelo');

// Para spiner
const resultadoContent = document.querySelector('#res-content');

const spinner = document.querySelector('.spinner')

llamarAddEventListeners();
function llamarAddEventListeners() {
    llamarModal.addEventListener('click', () => {
        modal.showModal()
    });
    cerrarModal.addEventListener('click', () => {
        modal.close();
    });
    consultar.addEventListener('click', llamarApi)
}

function limpiarHTML(limpiar) {
    while (limpiar.firstChild) {
        limpiar.removeChild(limpiar.firstChild);
    }
}


function llamarApi() {

    // seleccionando datos desde html
    const aerolinea = document.querySelector('#aerolinea').value.trim();
    const origen = document.querySelector('#origen').value.trim();
    const destino = document.querySelector('#destino').value.trim();
    const fecha = document.querySelector('#fecha').value.trim();
    const hora = document.querySelector('#hora').value.trim();
    const distancia = document.querySelector('input[type="number"]').value.trim();
    const distanciaKm = parseFloat(distancia)

    // validadciones

    if (!aerolinea || !origen || !destino || !fecha || !hora || !distanciaKm) {
        alerta('Debes llenar todos los campos');
        return;
    }

    let formatoHora = hora;
    if (hora.length === 5) {
        formatoHora += ":00"
    }

    const fechaPartida = `${fecha}T${hora}`;
    console.log(fechaPartida)

    // console.log({aerolinea, origen, destino, fechaPartida, distanciaKm});

    //objeto de api
    let datosAerolinea = {
        aerolinea,
        origen,
        destino,
        fechaPartida,
        distanciaKm
    }

    console.log(datosAerolinea)

    limpiarHTML(resultadoContent);

    mostrarSpinner(true);
    buttonDisabled(true);

    fetch("/api/predict", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(datosAerolinea)
    })
        .then(respuesta => {
            if (!respuesta.ok) throw new Error("UPS parece que la conexión API fallo");
            return respuesta.json();
        })
        .then(resultado => {
            setTimeout(() => {
                mostrarSpinner(false)
                buttonDisabled(false)
                insertarResultado(resultado);
            }, 3000);
        })
        .catch(error => {
            mostrarSpinner(false)
            console.error(error);
            alerta("Parece que fallo la conexión con nuestra API");
        })
        // .finally(() => );
}

function alerta(texto) {
    const consultarAlerta = document.querySelector('#alerta');

    limpiarHTML(consultarAlerta);

    const nuevaAlerta = document.createElement('P');
    nuevaAlerta.textContent = texto;
    nuevaAlerta.classList.add('alerta');

    consultarAlerta.appendChild(nuevaAlerta);

    setTimeout(() => {
        nuevaAlerta.remove();
    }, 3000);
}

function insertarResultado({ prevision, probabilidad }) {
    limpiarHTML(resultadoContent)

    let contenedorDiv = document.createElement('div');
    contenedorDiv.classList.add('mt-2', 'text-center', 'p-2', 'shadow-lg');

    const tituloDiv = document.createElement('P');
    tituloDiv.textContent = 'El resultado de la previsión es: '
    tituloDiv.classList.add('font-bold', 'mt-2', 'p-2');

    const estadoPrev = document.createElement('p');
    estadoPrev.classList.add('mt-4', 'p-2', 'text-bold');
    estadoPrev.textContent = prevision;

    const estadoProb = document.createElement('p');
    estadoProb.classList.add('mt-4', 'p-2', 'text-bold');
    estadoProb.textContent = probabilidad;

    contenedorDiv.appendChild(tituloDiv);
    contenedorDiv.appendChild(estadoPrev);
    contenedorDiv.appendChild(estadoProb);

    resultadoContent.appendChild(contenedorDiv);

    resetInputs();
}

function resetInputs() {
    formulario.reset();
}

function mostrarSpinner(mostar) {
    if (mostar) {
        spinner.classList.remove('hidden');
        return;
    }
    spinner.classList.add('hidden');
}

function buttonDisabled(bloquear) {
    consultar.disabled = bloquear;

    if (bloquear) {
        consultar.classList.add('opacity-50', 'cursor-not-alllowed');
        return;
    }
    consultar.classList.remove('opacity-50', 'cursor-not-alllowed');
}