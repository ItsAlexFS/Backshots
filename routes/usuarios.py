import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt, get_jwt_identity
from flask_bcrypt import Bcrypt

from config.db import get_db_connection

import os
from dotenv import load_dotenv

#cargar variables de entorno
load_dotenv()
#creamos bp
usuarios_bp = Blueprint("usuarios", __name__)
#iniciamos bcrypt
bcrypt = Bcrypt()

@usuarios_bp.route("/registrar", methods=["POST"])
def registrar():
    data=request.get_json()

    nombre=data.get("nombre")
    email=data.get("email")
    password=data.get("password")

    #validacion
    if not nombre or not email or not password:
        return jsonify({"error": "Faltan datos"}), 400
    
    #obtener el cursor
    cursor = get_db_connection()

    try:
        #checar que el usuario no existe
        cursor.execute("SELECT * FROM usuarios WHERE email=%s", (email,))
        exist_user=cursor.fetchone()

        if exist_user:
            return jsonify({"error": "El usuario ya existe"}), 400
        
        #hashear password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # insertar el usuario en db

        cursor.execute("INSERT INTO usuarios (nombre, email, password) VALUES (%s, %s, %s)", (nombre, email, hashed_password))

        #guardamos registry
        cursor.connection.commit()

        return jsonify({"mensaje": "Usuario registrado"}), 201

    except Exception as e:
        return jsonify({"error":f"Error al registrar usuario: {str(e)}"}), 500

    finally:
        #cerrar cursor
        cursor.close()

@usuarios_bp.route("/login", methods=["POST"])
def login():
    data=request.get_json()
    email=data.get("email")
    password=data.get("password")

    if not email or not password:
        return jsonify({"error": "Faltan datos"}), 400
    
    cursor= get_db_connection()

    query= "SELECT password, id_usuario FROM usuarios WHERE email= %s"
    cursor.execute(query, (email,))


    usuario=cursor.fetchone()

    if usuario and bcrypt.check_password_hash(usuario[0], password):
        #generar jwt
        expires=datetime.timedelta(minutes=60)

        access_token=create_access_token(
            identity=str(usuario[1]),
            expires_delta=expires)
        
        cursor.close()
        
        return jsonify({"token": access_token}), 200
    else:
        return jsonify({"error": "Credenciales invalidas"}), 401
    
@usuarios_bp.route("/datos", methods=["GET"])
@jwt_required()
def datos():
    current_user=get_jwt_identity()
    cursor=get_db_connection()
    query="SELECT id_usuario, nombre, email FROM usuarios WHERE id_usuario=%s"
    cursor.execute(query, (current_user,))
    usuario=cursor.fetchone()
    cursor.close()
    if usuario:
        user_info = {
            "id_usuario": usuario[0],
            "nombre": usuario[1],
            "email": usuario[2]
        }
        return jsonify({"datos": user_info}), 200
    else:
        return jsonify({"error": "Usuario no encontrado"}), 404