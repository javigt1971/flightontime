package com.hackathon.demo.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import lombok.Getter;

@Getter
public class PredictionRequestDTO {
    @NotBlank(message = "La aerolínea es obligatoria")
    private String aerolinea;

    @NotBlank(message = "El origen es obligatorio")
    private String origen;

    @NotBlank(message = "El destino es obligatorio")
    private String destino;

    @NotBlank(message = "La fecha de partida es obligatoria")
    private String fechaPartida;  // Formato ISO: "2025-11-10T14:30:00"

    //@Getter
    @NotNull(message = "La distancia es obligatoria")
    private Integer distanciaKm;

}
