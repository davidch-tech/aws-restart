import boto3
from datetime import datetime

SERVICIOS = {
    "EC2 Instances":   {"cliente": "ec2",    "metodo": "describe_instances",       "clave": ["Reservations", "Instances"], "global": False},
    "S3 Buckets":      {"cliente": "s3",     "metodo": "list_buckets",             "clave": ["Buckets"],                  "global": True},
    "Lambda Functions":{"cliente": "lambda", "metodo": "list_functions",           "clave": ["Functions"],                "global": False},
    "VPCs":            {"cliente": "ec2",    "metodo": "describe_vpcs",            "clave": ["Vpcs"],                     "global": False},
    "Security Groups": {"cliente": "ec2",    "metodo": "describe_security_groups", "clave": ["SecurityGroups"],           "global": False},
}

def get_credentials():
    key_id        = input("AWS Access Key ID: ")
    secret_key    = input("AWS Secret Access Key: ")
    region        = input("Región (ej. us-east-1): ")
    session_token = input("AWS Session Token: ")
    return key_id, secret_key, region, session_token

def crear_sesion(key_id, secret_key, region, session_token):
    return boto3.Session(
        aws_access_key_id=key_id,
        aws_secret_access_key=secret_key,
        region_name=region,
        aws_session_token=session_token
    )

def escanear(session, nombre, config):
    try:
        if config["global"]:
            cliente = session.client(config["cliente"], region_name=None)
        else:
            cliente = session.client(config["cliente"])

        metodo   = getattr(cliente, config["metodo"])
        response = metodo()
        claves   = config["clave"]

        if len(claves) == 2:  # anidado (ej. EC2: Reservations -> Instances)
            recursos = []
            for reserva in response[claves[0]]:
                recursos.extend(reserva[claves[1]])
        else:                 # plano (ej. S3, Lambda, VPC)
            recursos = response[claves[0]]

        return recursos
    except Exception as e:
        print(f"  Error escaneando {nombre}: {e}")
        return []

def imprimir_header(region):
    print("=" * 60)
    print("           INVENTARIO AWS")
    print(f"  Fecha : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Región: {region}")
    print("=" * 60)

def imprimir_reporte(nombre, recursos):
    print(f"\n{'='*60}")
    print(f"{nombre} ({len(recursos)})")
    print('=' * 60)
    if not recursos:
        print("  Sin recursos")
        return
    for r in recursos:
        if isinstance(r, dict):
            campos = {k: v for k, v in r.items() if isinstance(v, (str, int, bool))}
            print("  " + " | ".join(f"{k}: {v}" for k, v in list(campos.items())[:4]))
        else:
            print(f"  {r}")

def imprimir_resumen(inventario):
    print(f"\n{'='*60}")
    print("RESUMEN DE INVENTARIO")
    print('=' * 60)
    print(f"  {'Recurso':<25} {'Cantidad':>8}")
    print(f"  {'-'*25} {'-'*8}")
    total = 0
    for nombre, recursos in inventario.items():
        print(f"  {nombre:<25} {len(recursos):>8}")
        total += len(recursos)
    print(f"  {'-'*25} {'-'*8}")
    print(f"  {'TOTAL':<25} {total:>8}")
    print('=' * 60)
    

if __name__ == "__main__":
    key_id, secret_key, region, session_token = get_credentials()
    session = crear_sesion(key_id, secret_key, region, session_token)

    imprimir_header(region)

    inventario = {}
    for nombre, config in SERVICIOS.items():
        recursos = escanear(session, nombre, config)
        imprimir_reporte(nombre, recursos)
        inventario[nombre] = recursos

    imprimir_resumen(inventario)
