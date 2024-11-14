import json
import os
import jwt
from datetime import datetime, timedelta, timezone

def handler(event, context):
    # Obtener el secreto desde las variables de entorno
    jwt_secret = os.getenv('JWT_SECRET')
    authorized_username = os.getenv('AUTHORIZED_USERNAME')
    authorized_password = os.getenv('AUTHORIZED_PASSWORD')

    if not jwt_secret:
        return {
            "statusCode": 500,
            "body": json.dumps("Error: JWT_SECRET no está configurado.")
        }
    
    # Obtener username y password desde la solicitud

    username = event.get("username")
    password = event.get("password")

    '''# Verificar que hayan proporsionado username y password
    if not username or not password:
        return {
            "statusCode": 400,
            "body": json.dumps("Error: Se requiere 'username' y 'password'.")
        }'''
    
    # Validar las credenciales
    if username != authorized_username or password != authorized_password:
        return {
            "statusCode": 401,
            "body": json.dumps("Error: Credenciales invalidas.")
        }

    # Datos del payload para el token
    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1) # Expira en 1 hora
    }

    # Genera el token JWT
    token = jwt.encode(payload, jwt_secret, algorithm="HS256")

    return {
        "statusCode": 200,
        "body": json.dumps({"token": token})
    }