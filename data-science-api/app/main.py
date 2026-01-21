from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Any, Dict
import pickle
import pandas as pd
from datetime import datetime

app = FastAPI(title="FlightOnTime API")


def load_pickle(path: str):
    # Carga un objeto serializado con pickle (.pkl).
    with open(path, "rb") as f:
        return pickle.load(f)


# Carga de artefactos del modelo (exportados desde el notebook DS) 
modelo = load_pickle("app/artifacts/modelo_entrenado.pkl")
print("modelo.classes_:", getattr(modelo, "classes_", None))
encoders: Dict[str, Any] = load_pickle("app/artifacts/encoder.pkl")
features_modelo = load_pickle("app/artifacts/features_modelo.pkl")

# Encoders entrenados (LabelEncoder) para variables categóricas
le_aerolinea = encoders.get("le_aerolinea")
le_origen = encoders.get("le_origen")
le_destino = encoders.get("le_destino")

# Formato de entrada (uso interno / Data Science) 
class FlightRequest(BaseModel):
    AIRLINE: str
    ORIGIN: str
    DEST: str

    # Fecha: se puede enviar como FL_DATE o como MONTH + DAY_OF_WEEK
    FL_DATE: Optional[str] = Field(None, description="YYYY-MM-DD")
    MONTH: Optional[int] = Field(None, ge=1, le=12)
    DAY_OF_WEEK: Optional[int] = Field(None, ge=1, le=7)

    # Hora: se puede enviar como DEP_TIME o como DEP_TIME_HOUR
    DEP_TIME: Optional[Any] = Field(None, description="1345 o '13:45'")
    DEP_TIME_HOUR: Optional[int] = Field(None, ge=0, le=23)

    # Distancia: se puede enviar como DISTANCE_KM o como DISTANCE (millas)
    DISTANCE_KM: Optional[float] = Field(None, ge=0)
    DISTANCE: Optional[float] = Field(None, ge=0, description="millas")


def parse_dep_time_hour(dep_time: Any) -> int:  
    """
    Convierte la hora de salida a hora (0..23).

    Acepta:
      - 1345 (int) -> 13
      - "13:45" -> 13
      - "1345" -> 13
    """ 
    if isinstance(dep_time, int):
        return dep_time // 100
    s = str(dep_time).strip()
    if ":" in s:
        return int(s.split(":")[0])
    if s.isdigit():
        return int(s) // 100
    raise ValueError(f"DEP_TIME inválido: {dep_time}")


def month_and_dow_from_date(date_str: str):
    """
    A partir de FL_DATE (YYYY-MM-DD) retorna:
    - MONTH (1..12)
    - DAY_OF_WEEK (1..7, lunes=1)
    """
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.month, dt.weekday() + 1  # 1..7


def safe_label_encode(le, value: str, field_name: str) -> int:
    """
    Aplica LabelEncoder de forma segura.
    Si llega una categoría no vista durante entrenamiento, retorna 400 con mensaje claro.
    """
    if le is None:
        raise HTTPException(status_code=500, detail=f"Encoder no disponible: {field_name}")
    value = value.strip()
    if value not in le.classes_:
        raise HTTPException(status_code=400, detail=f"Valor no visto para {field_name}: '{value}'")
    return int(le.transform([value])[0])


def build_features(req: FlightRequest) -> pd.DataFrame:
    """
    Convierte el request (DS) a la matriz de features que el modelo espera:
    - Deriva MONTH/DAY_OF_WEEK desde FL_DATE si viene disponible
    - Deriva DEP_TIME_HOUR desde DEP_TIME si viene disponible
    - Convierte DISTANCE (millas) a DISTANCE_KM si corresponde
    - Aplica encoders y alinea columnas según features_modelo.pkl
    """
    # 1) MONTH + DAY_OF_WEEK (desde FL_DATE o campos directos)
    month = req.MONTH
    dow = req.DAY_OF_WEEK
    if req.FL_DATE:
        month, dow = month_and_dow_from_date(req.FL_DATE)

    if month is None or dow is None:
        raise HTTPException(status_code=400, detail="Envía FL_DATE o MONTH y DAY_OF_WEEK.")

    # 2) DEP_TIME_HOUR (desde DEP_TIME o campo directo)
    dep_hour = req.DEP_TIME_HOUR
    if dep_hour is None:
        if req.DEP_TIME is None:
            raise HTTPException(status_code=400, detail="Envía DEP_TIME o DEP_TIME_HOUR.")
        dep_hour = parse_dep_time_hour(req.DEP_TIME)

    # 3) DISTANCE_KM (desde DISTANCE_KM o convertir millas -> km)
    dist_km = req.DISTANCE_KM
    if dist_km is None:
        if req.DISTANCE is None:
            raise HTTPException(status_code=400, detail="Envía DISTANCE_KM o DISTANCE (millas).")
        dist_km = float(req.DISTANCE) * 1.60934

    # 4) Construir fila de features (nombres internos del modelo)
    row = {
        "AIRLINE": safe_label_encode(le_aerolinea, req.AIRLINE, "AIRLINE"),
        "ORIGIN": safe_label_encode(le_origen, req.ORIGIN, "ORIGIN"),
        "DEST": safe_label_encode(le_destino, req.DEST, "DEST"),
        "DEP_TIME_HOUR": int(dep_hour),
        "MONTH": int(month),
        "DAY_OF_WEEK": int(dow),
        "DISTANCE_KM": float(dist_km),
    }

    # 5) Alinear columnas exactas esperadas por el modelo (lista + orden)
    X = pd.DataFrame([row]).reindex(columns=features_modelo, fill_value=0)
    return X


@app.get("/health")
def health():
    # Healthcheck básico para verificar que la API y el modelo están operativos.
    return {"status": "ok", "n_features": len(features_modelo)}


@app.post("/predict")
def predict(req: FlightRequest):
    """
    Endpoint de uso interno (DS) para pruebas/depuración.
    Devuelve predicción y probabilidad de retraso (clase 1).
    """
    X = build_features(req)
    proba = float(modelo.predict_proba(X)[0][1]) if hasattr(modelo, "predict_proba") else None
    pred = int(modelo.predict(X)[0])
    label = "Retrasado" if pred == 1 else "Puntual"
    return {"prediccion": label, "probabilidad_retraso": proba}


# Formato de entrada solicitado por el proyecto (para integración con Back-End)
class BackendFlightRequest(BaseModel):
    aerolinea: str
    origen: str
    destino: str
    fechaPartida: str  # ISO 8601: "2025-11-10T14:30:00" (puede venir con Z u offset)
    distanciaKm: float


def parse_fechaPartida(fechaPartida: str):
    """
    Convierte fechaPartida (ISO 8601) en variables internas requeridas por el modelo:
    - MONTH (1-12)
    - DAY_OF_WEEK (1-7, donde 1=Lunes)
    - DEP_TIME_HOUR (0-23)

    Ejemplos aceptados:
    - "2025-11-10T14:30:00"
    - "2025-11-10T14:30:00Z"
    - "2025-11-10T14:30:00+00:00"
    """
    s = fechaPartida.strip()
    
    # Soporte para formato UTC con "Z"
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
        
    dt = datetime.fromisoformat(s) # soporta con o sin zona horaria (offset)
    month = dt.month
    day_of_week = dt.weekday() + 1 # 1..7
    dep_time_hour = dt.hour        # 0..23
    return month, day_of_week, dep_time_hour


@app.post("/predict_backend")
def predict_backend(req: BackendFlightRequest):
    # 1) Derivar variables temporales internas desde fechaPartida
    month, dow, dep_hour = parse_fechaPartida(req.fechaPartida)

    # 2) Transformar variables categóricas usando los encoders entrenados
    #    (esto asegura consistencia con el modelo exportado)
    row = {
        "AIRLINE": safe_label_encode(le_aerolinea, req.aerolinea, "AIRLINE"),
        "ORIGIN": safe_label_encode(le_origen, req.origen, "ORIGIN"),
        "DEST": safe_label_encode(le_destino, req.destino, "DEST"),
        "DEP_TIME_HOUR": int(dep_hour),
        "MONTH": int(month),
        "DAY_OF_WEEK": int(dow),
        "DISTANCE_KM": float(req.distanciaKm),
    }

    # 3) Alinear columnas exactas esperadas por el modelo (lista + orden)
    X = pd.DataFrame([row]).reindex(columns=features_modelo, fill_value=0)

    # 4) Inferencia: prevision + probabilidad (clase 1 = Retrasado)
    proba = float(modelo.predict_proba(X)[0][1]) if hasattr(modelo, "predict_proba") else None
    pred = int(modelo.predict(X)[0])
    label = "Retrasado" if pred == 1 else "Puntual"

    # 5) Respuesta en el formato esperado por el proyecto (probabilidad con 2 decimales)
    prob_redondeada = round(proba, 2) if proba is not None else None
    return {"prevision": label, "probabilidad": prob_redondeada}
