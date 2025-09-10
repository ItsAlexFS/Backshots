from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config.db import get_db_connection

#crear bp
tareas_bp=Blueprint("tareas", __name__)

#crear un endpoint para obtener tareas
@tareas_bp.route("/obtener", methods=["GET"])
@jwt_required()
def get():

    #obtener el id del usuario
    current_user=get_jwt_identity()

    #conectar a la db
    cursor= get_db_connection()
    query= '''
        SELECT a.id_usuario, a.descripcion, b.nombre, b.email, a.creado_en
        FROM tareas as a
        INNER JOIN usuarios as b
        ON a.id_usuario=b.id_usuario
        WHERE a.id_usuario=%s
        '''
    
    cursor.execute(query, (current_user,))
    lista=cursor.fetchall()
    cursor.close()

    if not lista:
        return jsonify({"mensaje": "No tienes tareas"}), 404
    else:
        return jsonify({"tareas": lista}), 200

#crear endpoint con post recibiendo datos desde el body
@tareas_bp.route('/crear', methods=["POST"])
@jwt_required()
def crear():
    #obtener id del usuario
    current_user = get_jwt_identity()

    #obtener datos del body
    data=request.get_json()
    descripcion=data.get("descripcion")

    if not descripcion:
        return jsonify({"error": "Debes agregar una descripcion"}), 400


    #obtenemos el cursor
    cursor = get_db_connection()

    #hacemos insert
    try:
        cursor.execute("INSERT INTO tareas (descripcion, id_usuario) values (%s, %s)", (descripcion, current_user))
        cursor.connection.commit()
        return jsonify({"mensaje": "Tarea creada"}, 201)
    except Exception as e:
        return jsonify({"error":f"No se puede crear la tarea: {str(e)}"}), 500
    finally:
        cursor.close()

# Crear un endpoint usando PUT y pasando datos por el body y el url
@tareas_bp.route("/modificar/<int:id_tarea>", methods=["PUT"])
@jwt_required()
def modificar(id_tarea):

    current_user = get_jwt_identity()

    #obtener datos del body
    data=request.get_json()
    descripcion=data.get("descripcion")

    #verificar que la tarea exista y que pertenezca al usuario
    cursor=get_db_connection()
    query="SELECT * FROM tareas WHERE id_tarea=%s"
    cursor.execute(query, (id_tarea,))
    tarea=cursor.fetchone()
    #esto devuelve tarea = (1, 2, etc)

    if not tarea:
        cursor.close()
        return jsonify({"error": "La tarea no existe"}), 404
    if not tarea[1] == int(current_user): #tarea[1] es el id_usuario de la tarea, current_user es str y hay que convertirlo a int para comparar
        cursor.close()
        return jsonify({"error": "Credenciales invalidas"}), 401
    
    #actualizar data
    try:
        cursor.execute("UPDATE tareas SET descripcion=%s WHERE id_tarea=%s", (descripcion, id_tarea))
        cursor.connection.commit()
        return jsonify({"mensaje": "Tarea modificada"}), 200
    except Exception as e:
        return jsonify({"error": f"No se puede modificar la tarea: {str(e)}"}), 500
    finally:
        cursor.close()