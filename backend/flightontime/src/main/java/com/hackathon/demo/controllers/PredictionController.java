package com.hackathon.demo.controllers;

import com.hackathon.demo.dto.PredictionRequestDTO;
import com.hackathon.demo.dto.PredictionResponseDTO;
import jakarta.validation.Valid;
import org.springframework.http.*;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class PredictionController {

    // Instancia de RestTemplate (puedes inyectarla con @Autowired si prefieres)
    private final RestTemplate restTemplate = new RestTemplate();

    // URL del microservicio FastAPI (cámbiala si usas otro puerto o Docker)
    private static final String FASTAPI_URL = "http://localhost:8000/predict_backend";

    @PostMapping("/predict")
    public ResponseEntity<PredictionResponseDTO> predict(
            @Valid @RequestBody PredictionRequestDTO request) {

        // Preparamos el body JSON idéntico al que espera FastAPI
        Map<String, Object> requestBody = new HashMap<>();
        requestBody.put("aerolinea", request.getAerolinea());
        requestBody.put("origen", request.getOrigen());
        requestBody.put("destino", request.getDestino());
        requestBody.put("fecha_partida", request.getFechaPartida());
        requestBody.put("distancia_km", request.getDistanciaKm());
        
        // Headers obligatorios
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        // Entidad completa para enviar
        HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

        try {
            // Llamada POST al FastAPI
            ResponseEntity<PredictionResponseDTO> response = restTemplate.exchange(
                    FASTAPI_URL,
                    HttpMethod.POST,
                    entity,
                    PredictionResponseDTO.class
            );

            // Devolvemos exactamente lo que nos dio FastAPI
            return ResponseEntity.status(response.getStatusCode()).body(response.getBody());

        } catch (Exception e) {
            // Manejo básico de errores (puedes mejorarlo con tu GlobalExceptionHandler)
            Map<String, String> error = new HashMap<>();
            error.put("error", "No se pudo conectar con el servicio de predicción: " + e.getMessage());
            return ResponseEntity.status(HttpStatus.SERVICE_UNAVAILABLE).body(new PredictionResponseDTO("Error", 0.0));
        }
    }

    /**
     * Endpoint de health-check básico
     * Útil para verificar que la API está corriendo
     */
    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("API FlightOnTime - UP");
    }

}