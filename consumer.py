from kafka import KafkaConsumer
from kafka.structs import TopicPartition
import json
import matplotlib.pyplot as plt
from collections import deque

# Configuración del servidor y topic
kafka_server = 'lab9.alumchat.lol:9092'
topic = '18248'
group_id = 'grupo4'

# Inicialización del Kafka Consumer
consumer = KafkaConsumer(
    topic,
    group_id=group_id,
    bootstrap_servers=[kafka_server],
    #value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    auto_offset_reset='earliest',  # Para consumir mensajes desde el principio
    enable_auto_commit=False
)
partition = TopicPartition(topic, 0)
end_offset = consumer.end_offsets([partition])[partition]
last_commited_offset = consumer.committed(partition)
print("end offset", end_offset)
print("last comitted offset", last_commited_offset)

# Listas para almacenar los datos
all_temp = deque(maxlen=100)  # Usar deque para limitar los datos y hacer scroll
all_hume = deque(maxlen=100)
all_wind = deque(maxlen=100)

# # Configurar gráficos en vivo
plt.ion()  # Habilita el modo interactivo de matplotlib
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 6))

def decode_data(encoded_message):
    payload = int.from_bytes(encoded_message, 'big')
    temp_encoded = (payload >> 10) & 0x3FFF
    hum_encoded = (payload >> 3) & 0x7F
    wind_encoded = payload & 0x7
    
    # Decodificar valores
    temperatura = temp_encoded * 110 / (2**14 - 1)
    humedad = hum_encoded
    wind_directions = {0: 'N', 1: 'NO', 2: 'O', 3: 'SO', 4: 'S', 5: 'SE', 6: 'E', 7: 'NE'}
    direccion_viento = wind_directions[wind_encoded]
    
    return {
        "temperatura": round(temperatura, 2),
        "humedad": humedad,
        "direccion_viento": direccion_viento
    }


# Función para actualizar el gráfico
def actualizar_grafico():
    # Graficar Temperatura
    ax1.clear()
    ax1.plot(all_temp, label='Temperatura (°C)', color='r')
    ax1.set_title('Temperatura')
    ax1.legend()

    # Graficar Humedad
    ax2.clear()
    ax2.plot(all_hume, label='Humedad (%)', color='b')
    ax2.set_title('Humedad Relativa')
    ax2.legend()
    
    # Graficar Dirección del viento
    ax3.clear()
    ax3.plot(all_wind, label='Dirección', color='g')
    ax3.set_title('Dirección del viento')
    ax3.legend()

    # Actualizar gráficos en vivo
    plt.draw()
    plt.pause(5)  # Pausa para actualizar

# Recuperar mensajes anteriores
print("Recuperando historial...")
for mensaje in consumer:
    #payload = mensaje.value
    payload = decode_data(mensaje.value)
    
    all_temp.append(payload['temperatura'])
    all_hume.append(payload['humedad'])
    all_wind.append(payload['direccion_viento'])
    
    if mensaje.offset == end_offset - 1:
        break

actualizar_grafico()

# Ciclo para consumir y procesar datos
try:
    print("Recibiendo mensajes...")
    for mensaje in consumer:
        # Imprimir el mensaje
        #print ("%s:%d:%d: key=%s value=%s" % (mensaje.topic, mensaje.partition,
        #                                      mensaje.offset, mensaje.key, mensaje.value))
        
        # Procesar el mensaje y actualizar listas de datos
        #payload = mensaje.value
        payload = decode_data(mensaje.value)

        print(f"Recibido: {payload}")
        
        all_temp.append(payload['temperatura'])
        all_hume.append(payload['humedad'])
        all_wind.append(payload['direccion_viento'])
        
        # Llamar a la función de actualización de gráficos
        actualizar_grafico()

except KeyboardInterrupt:
    print("Interrumpido por el usuario.")
finally:
    plt.ioff()
    plt.show()  # Mostrar el gráfico final una vez que se detenga el proceso
    consumer.close()
