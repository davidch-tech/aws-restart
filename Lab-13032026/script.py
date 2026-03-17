import boto3

# Configuración
BUCKET_NAME = input("Nombre del bucket: ")  # Reemplaza con el tuyo
FILE_NAME = input("Nombre del archivo: ")

def subir_archivo():
    # Creamos el cliente de S3
    # Boto3 busca automáticamente en ~/.aws/credentials
    s3 = boto3.client('s3')

    # Crear un archivo rápido para subir
    with open(FILE_NAME, 'w') as f:
        f.write("Hola! Este archivo se subio usando Boto3 y llaves fijas.")

    try:
        print(f"Subiendo {FILE_NAME} a {BUCKET_NAME}...")
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_NAME)
        print("✅ ¡Subida exitosa!")
    except Exception as e:
        print(f"❌ Error al subir: {e}")

if __name__ == "__main__":
    subir_archivo()