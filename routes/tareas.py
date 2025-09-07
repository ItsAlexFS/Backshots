from flask import Blueprint, request, jsonify
from config.db import get_db_connection

#crear bp
tareas_bp=Blueprint("tareas", __name__)

#crear un endpoint para obtener tareas
@tareas_bp.route("/obtener", methods=["GET"])
def get():
    return jsonify({"mensaje": "Estas son tus tareas"})

#crear endpoint con post recibiendo datos desde el body
@tareas_bp.route('/crear', methods=["POST"])
def crear():
    #obtener datos del body
    data=request.get_json()
    descripcion=data.get("descripcion")


    #obtenemos el cursor
    cursor = get_db_connection()

    #hacemos insert
    try:
        cursor.execute("INSERT INTO tareas (descripcion) values (%s)", (descripcion,))
        cursor.connection.commit()
        return jsonify({"mensaje": "Tarea creada"}, 201)
    except Exception as e:
        return jsonify({"error":f"No se puede crear la tarea: {str(e)}"}), 500
    finally:
        cursor.close()

# Crear un endpoint usando PUT y pasando datos por el body y el url
@tareas_bp.route("/modificar/<int:user_id>", methods=["PUT"])
def modificar(user_id):
    #obtener datos del body
    data=request.get_json()
    descripcion=data.get("descripcion")


    return jsonify({"saludo": descripcion})    