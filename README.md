# Kafka Producer-Consumer Weather Data Simulation

Este proyecto contiene dos scripts de Python que utilizan Apache Kafka para simular y graficar datos meteorológicos. 

## Contenidos

- [Descripción](#descripción)
- [Requisitos](#requisitos)
- [Configuración del Entorno](#configuración-del-entorno)
- [Instrucciones de Uso](#instrucciones-de-uso)
- [Ejecución de los Scripts](#ejecución-de-los-scripts)
- [Notas Adicionales](#notas-adicionales)

## Descripción

### Producer
El archivo `producer.py` simula la generación de lecturas de sensores de temperatura, humedad y dirección del viento, enviándolas al servidor Kafka configurado.

### Consumer
El archivo `consumer.py` se suscribe al topic Kafka para consumir los datos de los sensores, graficándolos en tiempo real mediante `matplotlib`.

## Requisitos

- **Python 3.6 o superior**
- **Apache Kafka** (configurado en el servidor y con un topic definido)
- **Ambiente Conda**

## Configuración del Entorno

### Crear el Entorno Conda

Este proyecto incluye un archivo `requirements.txt` que contiene todas las dependencias necesarias. Para crear el ambiente de Conda y configurarlo con los requerimientos del proyecto, sigue estos pasos:

1. **Clona el repositorio** (si es necesario):
    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```
2. **Crear el entorno de Conda**
    
    Desde la carpeta del repositorio:

    ```bash
    conda create --name <env_name> --file requirements.txt
    ```

3. **Activar el entorno**

    ```bash
    conda activate <env_name>
    ```
## Instrucciones de Uso

1. **Ejecutar el Producer**
2. **Ejecutar el Consumer**

## Ejecución de los Scripts

### Producer
Con el entorno de Conda activado, inicia el producer con:
```bash
python producer.py
```

### Consumer
Inicia el consumer con:
```bash
python consumer.py
```

## Notas Adicionales

- **Historial de Datos**: El consumer recupera mensajes anteriores antes de comenzar la visualización en tiempo real.
