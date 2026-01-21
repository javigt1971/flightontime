package com.hackathon.demo.dto;
import lombok.AllArgsConstructor;
import lombok.Data;

@Data
@AllArgsConstructor
public class PredictionResponseDTO {
    private String prevision;     // "Puntual" o "Retrasado"
    private double probabilidad;  // 0.0 a 1.0

}
