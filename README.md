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

## ⚙️Cómo ejecutar el proyecto (explicado simple)
**Paso 1: Entrenar el modelo (equipo DS)**
- Abrir el notebook en Google Colab.
- Ejecutar todas las celdas.
- Al final se generará un archivo del modelo (por ejemplo model.pkl).
  
**Paso 2: Colocar el modelo en el Back-End**
- Copiar el archivo del modelo dentro del proyecto Java (o configurarlo para que lo lea desde un microservicio Python).
  
**Paso 3: Ejecutar la API**
En la carpeta del proyecto Java:

Bash
./mvnw spring-boot:run

La API quedará disponible en:
http://localhost:8080/predict

**Paso 4: Probar la API**
Puedes usar:
- Postman
- Una interfaz simple creada por el equipo

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

