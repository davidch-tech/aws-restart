#!/bin/bash

echo "--- PASO 1: CONFIGURACIÓN DE CREDENCIALES ---"
# Lanza el asistente oficial de AWS
aws configure

echo -e "\n--- PASO 2: CREACIÓN DE CARPETA LOCAL ---"
read -p "Nombre de la carpeta local: " FOLDER_NAME

if [ -d "$FOLDER_NAME" ]; then
    echo "La carpeta ya existe."
else
    mkdir "$FOLDER_NAME"
    echo "Carpeta '$FOLDER_NAME' creada."
fi

echo -e "\n--- PASO 3: CREACIÓN DE BUCKET S3 ---"
read -p "Nombre del bucket (se convertirá a minúsculas): " RAW_BUCKET
# Convertir a minúsculas automáticamente
BUCKET_NAME=$(echo "$RAW_BUCKET" | tr '[:upper:]' '[:lower:]')

# Ejecutar la creación
aws s3api create-bucket \
    --bucket "$BUCKET_NAME" \
    --region us-west-2 \
    --create-bucket-configuration LocationConstraint=us-west-2

# Verificar resultado
if [ $? -eq 0 ]; then
    echo "¡Bucket '$BUCKET_NAME' listo!"
else
    echo "Error al crear el bucket. Revisa si el nombre es único o tus credenciales."
fi

echo -e "\n--- RESUMEN FINAL ---"
aws s3 ls