# Directorio donde se guardarán los certificados y claves
#CERT_DIR="/home/cvp/Entrega-2-iot/app/certs"
CERT_DIR="/home/cvp/Entrega-2-iot/mosquitto/certs"

# Nombre del cliente base
CLIENT_BASE_NAME="ClaudiaPortatil"

# Crear el directorio si no existe
mkdir -p "$CERT_DIR"

# Generar un certificado de autoridad (CA)
openssl req -new -x509 -days 3650 -extensions v3_ca -keyout "$CERT_DIR/ca.key" -out "$CERT_DIR/ca.crt" -subj "/CN=MyCA/OU=MyOrganization/C=US"

# Generar una clave privada y un certificado autofirmado para el servidor
openssl req -new -nodes -newkey rsa:2048 -keyout "$CERT_DIR/server.key" -out "$CERT_DIR/server.csr" -subj "/CN=localhost"
openssl x509 -req -days 365 -in "$CERT_DIR/server.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial -out "$CERT_DIR/server.crt"

# Limpiar archivos temporales
rm "$CERT_DIR/server.csr" "$CERT_DIR/ca.srl"

# Generar claves privadas y certificados autofirmados para cada cliente
for ((i=1; i<=4; i++)); do
    CLIENT_NAME="${CLIENT_BASE_NAME}${i}"
    openssl req -new -nodes -newkey rsa:2048 -keyout "$CERT_DIR/$CLIENT_NAME.key" -out "$CERT_DIR/$CLIENT_NAME.csr" -subj "/CN=$CLIENT_BASE_NAME"
    openssl x509 -req -days 365 -in "$CERT_DIR/$CLIENT_NAME.csr" -CA "$CERT_DIR/ca.crt" -CAkey "$CERT_DIR/ca.key" -CAcreateserial -out "$CERT_DIR/$CLIENT_NAME.crt"
    # Limpiar archivos temporales
    rm "$CERT_DIR/$CLIENT_NAME.csr"
done

# Establecer los permisos adecuados
chmod 600 "$CERT_DIR"/*.key

echo "Certificados y claves generados con éxito en $CERT_DIR"
