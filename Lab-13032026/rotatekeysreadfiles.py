import boto3
import json

def obtener_credenciales():
    """Función 1: Solo obtiene las llaves de la caja fuerte"""
    secret_name = input("Nombre del secreto en AWS: ")
    region = "us-east-1"
    
    sm_client = boto3.client('secretsmanager', region_name=region)
    
    try:
        response = sm_client.get_secret_value(SecretId=secret_name)
        keys = json.loads(response['SecretString'])
        print("✅ Credenciales obtenidas.")
        # Retornamos las llaves para que otra función las use
        return keys['ACCESS_KEY'], keys['SECRET_KEY']
    except Exception as e:
        print(f"❌ Error en Secrets Manager: {e}")
        return None, None

def crear_cliente_s3(ak, sk):
    """Función 2: Recibe llaves y devuelve un objeto cliente de S3"""
    if not ak or not sk: return None
    
    return boto3.client(
        's3',
        aws_access_key_id=ak,
        aws_secret_access_key=sk
    )

def leer_archivo_especifico(s3_client):
    """Función 3: Recibe el cliente y busca el archivo"""
    try:
        # Listar buckets rápido para que el usuario vea qué hay
        buckets = s3_client.list_buckets()
        print(f"Buckets disponibles: {[b['Name'] for b in buckets['Buckets']]}")
        
        bn = input("Nombre del bucket: ")
        fn = input("Nombre del archivo: ")
        folder = input("Carpeta (opcional): ")
        
        path = f"{folder}/{fn}" if folder else fn
        
        print(f"Buscando {path}...")
        obj = s3_client.get_object(Bucket=bn, Key=path)
        contenido = obj['Body'].read().decode('utf-8')
        
        print("\nCONTENIDO DEL ARCHIVO:")
        print(contenido)
        
    except Exception as e:
        print(f"❌ Error al buscar archivo: {e}")

# --- BLOQUE PRINCIPAL (Orquestador) ---
if __name__ == "__main__":
    # 1. Obtenemos strings (llaves)
    access_key, secret_key = obtener_credenciales()
    
    if access_key:
        # 2. Convertimos llaves en un objeto 's3_client'
        cliente_s3 = crear_cliente_s3(access_key, secret_key)
        
        # 3. Pasamos el cliente a la función de búsqueda
        leer_archivo_especifico(cliente_s3)