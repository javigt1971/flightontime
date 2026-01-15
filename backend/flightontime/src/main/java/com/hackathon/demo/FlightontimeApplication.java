package com.hackathon.demo;

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class FlightontimeApplication implements CommandLineRunner {

	public static void main(String[] args) {
		SpringApplication.run(FlightontimeApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		System.out.println("Hola Equipo, H12-25-L-Equipo 18-Data Science");
		System.out.println("Proyecto MVP para predecir retrasos en vuelos usando Data Science y API en Java Spring Boot");
	}
}
