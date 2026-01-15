package com.hackathon.demo.exception;

public class FlightValidationException extends RuntimeException {
    public FlightValidationException(String message) {
        super(message);
    }
}
