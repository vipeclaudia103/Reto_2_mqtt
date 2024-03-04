import ssl
import random
from paho.mqtt import client as mqtt_client

# Configuración del cliente MQTT
broker_address = "Entrega-2"
port = 8883
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = "admin"  # Opcional, dependiendo de la configuración del broker
password = "admin" # Opcional, dependiendo de la configuración del broker
cert_path = "/home/cvp/Entrega-2-iot/mosquitto/certs/ClaudiaPortatil3.crt"
key_path = "/home/cvp/Entrega-2-iot/mosquitto/certs/ClaudiaPortatil3.key"
ca_cert = "/home/cvp/Entrega-2-iot/mosquitto/certs/ca.crt"


# Función de conexión al broker MQTT
def on_connect(client, userdata, flags, rc):
    print("Conectado al broker MQTT con resultado " + str(rc))
    # Suscribirse a un tema
    client.subscribe("topic/test")

# Función para manejar los mensajes recibidos
def on_message(client, userdata, msg):
    print("Mensaje recibido: " + msg.topic + " " + str(msg.payload))

# Configurar el cliente MQTT con TLS/SSL
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
client.tls_set(ca_certs=ca_cert, certfile=cert_path, keyfile=key_path, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS)
client.on_connect = on_connect
client.on_message = on_message

# Autenticación, si es necesaria
if username is not None and password is not None:
    client.username_pw_set(username, password)

# Conectar al broker MQTT
client.connect(broker_address, port)

# Iniciar el bucle de red para manejar la comunicación con el broker
client.loop_start()

# Publicar datos
client.publish("topic/test", "Hello, World!")

# Mantener la ejecución del programa para recibir mensajes
while True:
    pass
