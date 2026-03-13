import os

# 1. Definimos el rango y el archivo


inicio = int(input("Ingrese el número inicial (mínimo 1): "))
fin = int(input("Ingrese el número final (máximo 250): "))
archivo_salida = "141--Lab/results.txt"

if inicio < 1 or fin > 250 or inicio > fin:
    print("Por favor, ingrese un rango válido (1-250) y asegúrese de que el número inicial no sea mayor que el final.")
    exit(1)

print(f"Buscando primos entre {inicio} y {fin}...")

# 2. Creamos una lista vacía para guardar los primos que encontremos
lista_primos = []

# 3. EL BUCLE FOR: Vamos a pasar por cada número del 1 al 250
for num in range(inicio, fin + 1):
    if num < 2:
        continue # El 1 no es primo, saltamos al siguiente
    
    es_primo = True # Asumimos que es primo hasta que se demuestre lo contrario
    
    # Otro bucle para intentar dividir el 'num' por otros números
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            es_primo = False # Si la división es exacta, no es primo
            break # Dejamos de buscar, ya sabemos que no sirve
            
    # Si después de revisar, 'es_primo' sigue siendo True, lo guardamos
    if es_primo:
        lista_primos.append(str(num))

# 4. Guardar los resultados en el archivo
try:
    with open(archivo_salida, "w") as f:
        # Convertimos la lista en una cadena de texto separada por comas
        f.write(", ".join(lista_primos))
    
    # 5. Verificación final
    print("¡Listo! Los primos han sido guardados.")
    print(f"Ubicación absoluta del archivo: {os.path.abspath(archivo_salida)}")
    
except Exception as e:
    print(f"Hubo un error al guardar: {e}")