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
    #value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def encode_data(temperatura, humedad, direccion_viento):
    # Convertir temperatura a un valor de 14 bits
    temp_encoded = int(temperatura * (2**14 - 1) / 110)
    # Humedad en 7 bits
    hum_encoded = int(humedad)
    # Dirección de viento en 3 bits
    wind_directions = {'N': 0, 'NO': 1, 'O': 2, 'SO': 3, 'S': 4, 'SE': 5, 'E': 6, 'NE': 7}
    wind_encoded = wind_directions[direccion_viento]
    
    # Combinar los bits en un entero de 24 bits
    payload = (temp_encoded << 10) | (hum_encoded << 3) | wind_encoded
    # Convertir a bytes
    return payload.to_bytes(3, 'big')


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
        encoded_message = encode_data(data['temperatura'], data['humedad'], data['direccion_viento'])
        producer.send(topic, value=encoded_message)
        
        # Espera entre 15 y 30 segundos antes de enviar el siguiente mensaje
        #time.sleep(random.randint(15, 30))
        time.sleep(3)

except KeyboardInterrupt:
    print("Interrumpido. Cerrando el producer.")
finally:
    producer.close()
