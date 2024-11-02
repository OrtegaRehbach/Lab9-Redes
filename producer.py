from kafka import KafkaProducer
import json
import random
import time
from datetime import datetime

# Configuración del servidor Kafka
kafka_server = 'lab9.alumchat.lol:9092'
topic = '18248'

# Inicialización del Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=kafka_server,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generar_datos():
    # Genera valores de los sensores
    temperatura = round(random.normalvariate(55, 15), 2)  # Distribución normal centrada en 55
    humedad = int(random.normalvariate(55, 15))  # Distribución normal centrada en 55
    direccion_viento = random.choice(['N', 'NO', 'O', 'SO', 'S', 'SE', 'E', 'NE'])
    
    # Estructura los datos en JSON
    return {
        "timestamp": datetime.now().isoformat(),
        "temperatura": temperatura,
        "humedad": humedad,
        "direccion_viento": direccion_viento
    }

try:
    while True:
        # Generar y enviar datos
        data = generar_datos()
        print(f"Enviando datos: {data}")
        producer.send(topic, value=data)
        
        # Espera entre 15 y 30 segundos antes de enviar el siguiente mensaje
        time.sleep(random.randint(15, 30))

except KeyboardInterrupt:
    print("Interrumpido. Cerrando el producer.")
finally:
    producer.close()
