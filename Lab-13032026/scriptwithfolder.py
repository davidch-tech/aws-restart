import boto3



def upload_file():
    # Creamos el cliente de S3
    # Boto3 busca automáticamente en ~/.aws/credentials
    # Configuración
    BUCKET_NAME = input("Nombre del bucket: ")  # Reemplaza con el tuyo
    FILE_NAME = input("Nombre del archivo: ")
    FOLDER_NAME = input("Nombre de la carpeta (opcional): ")
    if not FILE_NAME:
        print("❌ El nombre del archivo no puede estar vacío.")
        return
    s3 = boto3.client('s3')
    FILE_PATH = f"{FOLDER_NAME}/{FILE_NAME}" if FOLDER_NAME else FILE_NAME
    try:
         #cargar el archivo localmente en S3
        print(f"Subiendo {FILE_NAME} a {BUCKET_NAME}/{FOLDER_NAME}....")
        s3.upload_file(FILE_NAME, BUCKET_NAME, FILE_PATH)
        print("✅ ¡Subida exitosa!")
    except Exception as e:
        print(f"❌ Error al subir: {e}")
        
    
if __name__ == "__main__":
    upload_file()
