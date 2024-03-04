import ssl
import random
import time
from paho.mqtt import client as mqtt_client

# Configuración del cliente MQTT
broker_address = "Entrega-2"
port = 8883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "admin"  # Opcional, dependiendo de la configuración del broker
password = "admin"  # Opcional, dependiendo de la configuración del broker
cert_path = "/home/cvp/Entrega-2-iot/mosquitto/certs/ClaudiaPortatil4.crt"
key_path = "/home/cvp/Entrega-2-iot/mosquitto/certs/ClaudiaPortatil4.key"
ca_cert = "/home/cvp/Entrega-2-iot/mosquitto/certs/ca.crt"
topic = "topic/test"

# Función de conexión al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado " + str(rc))

# Configurar el cliente MQTT con TLS/SSL
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
client.tls_set(ca_certs=ca_cert, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect

# Autenticación, si es necesaria
if username is not None and password is not None:
    client.username_pw_set(username, password)

# Conectar al broker MQTT
client.connect(broker_address, port)

# Iniciar el bucle de red para manejar la comunicación con el broker
client.loop_start()

# Publicar datos
msg_count = 0
while True:
    value = f"Value: {msg_count}"
    client.publish(topic, value)
    print(f"Publicado: {value}")
    msg_count += 1
    time.sleep(1)
