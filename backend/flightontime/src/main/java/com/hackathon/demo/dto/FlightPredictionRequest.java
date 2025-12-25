package com.hackathon.demo.dto;

import java.time.LocalDateTime;

public record FlightPredictionRequest(
    String aerolinea,
    String origen,
    String destino,
    LocalDateTime fechaPartida,
    Float distanciaKm
) {
}
