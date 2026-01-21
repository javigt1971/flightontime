# API de Inferencia (Data Science) – FlightOnTime ✈️

Microservicio de inferencia en **FastAPI** que carga el modelo entrenado de predicción de retrasos y expone endpoints HTTP para consumo desde Back-End.

---

## ✅ Endpoints

### `GET /health`

Verifica que el servicio esté activo y que el modelo cargó correctamente.

**Respuesta (ejemplo):**
```json
{
  "status": "ok",
  "n_features": 7
}
```

### `POST /predict_backend` (formato solicitado por el proyecto)

Endpoint recomendado para integración con Back-End.

**Entrada (JSON):**
```json
{
  "aerolinea": "AZ",
  "origen": "GIG",
  "destino": "GRU",
  "fechaPartida": "2025-11-10T14:30:00",
  "distanciaKm": 350
}
```

**Salida (JSON):**
```json
{
  "prevision": "Retrasado",
  "probabilidad": 0.78
}
```

La API deriva internamente mes/día/hora desde `fecha_partida`, aplica encoders y alinea columnas según `features_modelo.pkl` para asegurar consistencia con el modelo.

### `POST /predict` (uso interno / DS)

Endpoint útil para pruebas internas con el formato DS (AIRLINE, ORIGIN, etc.).

---

## 🧩 Requisitos

- Python 3.12
- pip

---

## 📦 Artefactos del modelo (.pkl)

Por tamaño y buenas prácticas, los artefactos del modelo no se suben en GitHub.

Antes de ejecutar, debes colocar en:
```
data-science-api/app/artifacts/
```

los siguientes archivos (generados al ejecutar el notebook DS):

- `modelo_entrenado.pkl`
- `encoder.pkl`
- `features_modelo.pkl`

Los artefactos están disponibles vía enlace externo (Drive), agrupados en el archivo ***artifacts.zip*** 
y referenciados en Recursos, como pide No Country.

---

## ▶️ Ejecución local

Desde la carpeta `data-science-api/`:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**Abrir Swagger (documentación y pruebas):**
```
http://127.0.0.1:8000/docs
```

---

## 🧪 Prueba rápida (ejemplo real)

**Request a `/predict_backend`:**
```json
{
  "aerolinea": "DL",
  "origen": "ATL",
  "destino": "MIA",
  "fechaPartida": "2015-07-20T08:10:00",
  "distanciaKm": 957
}
```

**Response (ejemplo):**
```json
{
  "prevision": "Puntual",
  "probabilidad": 0.27
}
```

---

## 📝 Notas

- Si llega una aerolínea/aeropuerto no visto durante entrenamiento, la API responde con `400` y un mensaje claro.
- La probabilidad se entrega redondeada a 2 decimales para cumplir el formato esperado.

