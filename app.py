from flask import Flask
import os
from dotenv import load_dotenv
from config.db import init_db, mysql

#importar ruta del bp
from routes.tareas import tareas_bp
from routes.usuarios import usuarios_bp

load_dotenv()

def create_app(): #creando app
    app = Flask(__name__)

    init_db(app)
    #registrar bp
    app.register_blueprint(tareas_bp, url_prefix="/tareas")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

    return app

app=create_app()

if __name__=="__main__":
    #obtenemos el port
    port = int(os.getenv("PORT", 8080))
    #corremos app
    app.run(host="0.0.0.0", port=port, debug=True)