# ✈️ FlightOnTime – Predicción de retrasos en vuelos

## 🌍 Contexto
Viajar en avión debería ser sinónimo de puntualidad, pero los retrasos siguen siendo uno de los grandes dolores de cabeza para pasajeros, aerolíneas y aeropuertos.  
**FlightOnTime** nace como un proyecto de hackathon cuyo objetivo es anticipar si un vuelo saldrá a tiempo o sufrirá demoras, utilizando ciencia de datos y una API accesible.

---
## 🎯 Objetivo del proyecto
Construir un **MVP (Producto Mínimo Viable)** que:
- Reciba información básica de un vuelo.
- Procesarla con un modelo entrenado.
- Responder si el vuelo será **Puntual** o **Retrasado**.  
- Entregar también la **probabilidad** asociada a esa predicción.
Ejemplo:
“Retrasado con probabilidad 0.78”

---
## 🧠 Como funciona el proyecto:
**Parte 1: Ciencia de Datos**
El equipo DS:

1. Analiza los datos de vuelos.
2. Limpia y prepara la información.
3. Crea variables útiles (hora del día, día de la semana, aerolínea, etc.).
4. Entrena un modelo de clasificación (por ejemplo, Logistic Regression o Random Forest).
5. Evalúa su desempeño.
6. Guarda el modelo en un archivo (model.pkl o similar).
Ese archivo es el que luego usará el Back-End.
##
**Parte 2: Back-End**
El equipo BE:

1. Construye una API REST con Spring Boot.
2. Crea un endpoint llamado **/predict.**
3. Recibe un JSON con los datos del vuelo.
4. Carga el modelo entrenado (o llama a un microservicio Python).
5. Devuelve la predicción y la probabilidad.
6. Valida que los datos estén completos y correctos.
##
## Arquitectura general

```text
Cliente (Postman / App / www.flightontime.cl)
   ↓
API Back-End (Java / Spring Boot)
   ↓
API de Inferencia (Python / FastAPI)
   ↓
Modelo de ML (.pkl) + encoders + lista de features

```
---
## 📥 Formato de entrada y salida

**Entrada que recibe la API**

Json    
{    
  "aerolinea": "AZ",    
  "origen": "GIG",    
  "destino": "GRU",    
  "fechaPartida": "2025-11-10T14:30:00",    
  "distanciaKm": 350    
}    

**Respuesta que entrega la API** 

Json    
{    
  "prevision": "Retrasado",    
  "probabilidad": 0.78    
}    

## 🧪 Ejemplos de uso
**Ejemplo 1 – Vuelo puntual**

Json    
{    
  "prevision": "Puntual",    
  "probabilidad": 0.22    
}    

**Ejemplo 2 – Vuelo retrasado**

Json    
{    
  "prevision": "Retrasado",    
  "probabilidad": 0.81    
}    

**Ejemplo 3 – Error por datos incompletos**

Json    
{    
  "error": "El campo 'origen' es obligatorio"    
}    

## ⚙️Cómo ejecutar el proyecto 
**Paso 1: Entrenar el modelo (Equipo Data Science)**
- Abrir el notebook de entrenamiento en Google Colab.
- Ejecutar todas las celdas.
- Al final se generan los artefactos del modelo:
    - modelo_entrenado.pkl
    - encoder.pkl
    - features_modelo.pkl
           
Estos archivos representan el modelo final y no se versionan en GitHub por su tamaño.
#  
**Paso 2: Ejecutar la API de Inferencia (Data Science)**
El equipo de Data Science expone el modelo mediante un microservicio en Python (FastAPI), que será consumido por el Back-End.

Desde la carpeta data-science-api:

```text
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
La API queda disponible en:
- API: http://127.0.0.1:8000
- Swagger (documentación interactiva): http://127.0.0.1:8000/docs
- Healthcheck: http://127.0.0.1:8000/health
# 
**Paso 3: Ejecutar el Back-End (Spring Boot)**
El Back-End NO carga el modelo directamente, sino que consume la API de inferencia de Data Science.

Desde la carpeta del proyecto Java:

./mvnw spring-boot:run

El endpoint principal queda disponible en:
POST http://localhost:8080/predict
#
**Paso 4: Probar el sistema**
- El Back-End envía la información del vuelo a la API DS.
- La API DS devuelve:
    -  Prevision (Puntual / Retrasado)
    -  Probabilidad asociada.
- El Back-End responde al cliente final.

Las pruebas pueden realizarse con:
- Postman
- cURL
- Swagger de la API DS
---  
## 📘 Datos utilizados
El proyecto usa un conjunto de datos con información básica de vuelos, como:
- Aerolínea
- Origen
- Destino
- Fecha y hora
- Distancia

## 🔧 Funcionalidades opcionales 
- Estadísticas agregadas (por ejemplo, porcentaje de retrasos del día).
- Guardar las predicciones en una base de datos.
- Dashboard visual en tiempo real.
- Integración con datos de clima.
- Predicciones en lote (archivo CSV).
- Explicación de qué variables influyen más en la predicción.
- Contenerización con Docker.
- Pruebas automatizadas.

