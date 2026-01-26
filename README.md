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
- Entregar también la **probabilidad** asociada a esa previsión.
Ejemplo:
“Retrasado con probabilidad 0.78”

---
## 🧠 Parte 1: Ciencia de Datos (Equipo Data Science)

El equipo de Data Science: 

1. Analiza los datos de vuelos.
2. Limpia y prepara la información.
3. Crea variables útiles (hora del día, día de la semana, aerolínea, etc.).
4. Entrena un modelo de clasificación (por ejemplo, Logistic Regression o Random Forest).
5. Evalúa su desempeño.
6. Guarda el modelo en un archivo (model.pkl o similar).
Ese archivo es el que luego usará el Back-End.

## 🖥️ Parte 2: Back-End (Equipo Back-End)
El equipo Back-End:

1. Construye una API REST con Spring Boot.
2. Crea un endpoint llamado **/predict.**
3. Recibe un JSON con los datos del vuelo.
4. Carga el modelo entrenado (o llama a un microservicio Python).
5. Devuelve la predicción y la probabilidad.
6. Valida que los datos estén completos y correctos.
---
## 🏗️ Arquitectura general

```text
Cliente (Postman / App / www.flightontime.com)
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
  "fecha_partida": "2025-11-10T14:30:00",    
  "distancia_km": 350    
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

Endpoint principal:
**POST http://localhost:8080/predict**
#
**Paso 4: Probar el sistema**
- El Back-End envía la información del vuelo a la API Data Science.
- La API Data Science devuelve:
    -  Previsión (Puntual / Retrasado)
    -  Probabilidad asociada.
- El Back-End responde al cliente final.

Pruebas recomendadas:
- Postman
- Swagger de la API Data Science
---  
## 📘 Datos utilizados

El proyecto utiliza un conjunto de datos con información básica de vuelos, como:

- Aerolínea
- Origen
- Destino
- Fecha y hora
- Distancia

**Fuente del dataset (Kaggle):** [Kaggle - Flight Delay and Cancellation Dataset 2019-2023](https://www.kaggle.com/datasets/patrickzel/flight-delay-and-cancellation-dataset-2019-2023)


---
## 🛠️ Herramientas utilizadas

Para desarrollar el MVP se utilizaron herramientas y tecnologías en distintas áreas:

### 🧑‍💻 Lenguajes de programación

* **Python**: entrenamiento del modelo y API de inferencia (FastAPI).
* **Java**: API principal del sistema (Spring Boot).
* **JavaScript**: soporte para el ecosistema web (cliente / front si aplica).

### 🎨 Front-End y tecnologías web

* **HTML**: estructura de interfaz web.
* **Tailwind CSS**: estilos rápidos y consistentes.
* **Vite**: entorno de desarrollo y build para el Front-End.

### 🧠 Ciencia de datos

* **Google Colab**: notebooks para análisis, limpieza y entrenamiento del modelo.
* **FastAPI**: microservicio de inferencia que expone predicción y probabilidad.
* **Swagger UI**: documentación interactiva generada automáticamente por FastAPI.

### ⚙️ Back-End

* **Spring Boot**: API principal que consume la API de inferencia y expone el endpoint `/predict`.
* **IntelliJ IDEA**: entorno de desarrollo utilizado para el Back-End.

### 🧪 Pruebas y consumo de API

* **Postman**: pruebas de endpoints y validación de requests/responses.

### 🌐 Control de versiones y repositorios

* **GitHub**: versionamiento, colaboración y repositorios del proyecto.

### 📋 Gestión y colaboración

* **Trello**: organización y seguimiento de tareas.
* **Google Docs / Google Sheets**: documentación y gestión colaborativa.
* **Google Meet / WhatsApp**: coordinación del equipo.
* **No Country**: entorno de colaboración y dinámica del hackathon/simulación.

### 🎥 Comunicación y presentaciones

* **OBS Studio**: grabación de demos y presentaciones.
* **Canva**: diseño de material visual y soporte de presentación.
---
## 🚀 Mejoras Propuestas y Oportunidades de Crecimiento
 
- Estadísticas agregadas (por ejemplo, porcentaje de retrasos del día).
- Guardar las predicciones en una base de datos.
- Dashboard visual en tiempo real.
- Integración con datos de clima.
- Contenerización con Docker.
- Pruebas automatizadas.

---
## 📚 Referencias
- [Tablero Trello del proyecto](https://trello.com/b/QmhQEbIF/proyecto-flightontime-%E2%9C%88%EF%B8%8F-predicci%C3%B3n-de-retrasos-de-vuelos)
- [Repositorio GitHub](https://github.com/javigt1971/flightontime)

