from flask import Flask

from extensions import db, login_manager

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================

app.config['SECRET_KEY'] = 'clave_super_segura'

#app.config['SQLALCHEMY_DATABASE_URI'] = (
 #   'mysql+pymysql://root:utWabMlSivSEEkcYhNNfjtCTdDiXyVNN@acela.proxy.rlwy.net:25475/railway'
#)
import os

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL'
)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# =========================
# INICIALIZAR EXTENSIONS
# =========================

db.init_app(app)

with app.app_context():
    try:
        db.engine.connect()
        print("MYSQL OK")
    except Exception as e:
        print("ERROR MYSQL:", e)

login_manager.init_app(app)

#login_manager.login_view = 'login'


# =========================
# IMPORTAR MODELOS
# =========================

from models.usuario import Usuario
from models.partido import Partido
from models.prediccion import Prediccion
from models.tabla_posiciones import TablaPosiciones


# =========================
# USER LOADER
# =========================

@login_manager.user_loader
def load_user(user_id):

    return Usuario.query.get(int(user_id))


# =========================
# IMPORTAR CONTROLADORES
# =========================

from controllers.auth_controller import *
from controllers.admin_controller import *
from controllers.usuario_controller import *

from controllers.tabla_controller import *
from controllers.grupo_controller import *
from controllers.usuario_controller import *

#app.register_blueprint(tabla_bp)


@app.route('/test_prueba')
def test_prueba1():
    return "Aplicación funcionando"

@app.errorhandler(Exception)
def error_general(error):
    return f"ERROR: {str(error)}", 500

@app.route("/")
def home():

    print("ENTRO A HOME")

    return "HOME OK"

#print(app.url_map)


@app.route('/health')
def health():

    return 'OK', 200

print("APP CARGADA COMPLETAMENTE")
# =========================
# EJECUTAR APP
# =========================

if __name__ == '__main__':

    app.run()
