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

print("INICIANDO APP")

db.init_app(app)

print("DB INICIALIZADA")

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
print("ANTES CONTROLADORES")

from controllers.auth_controller import *
from controllers.admin_controller import *
from controllers.usuario_controller import *

from controllers.tabla_controller import *
from controllers.grupo_controller import *
from controllers.usuario_controller import *
print("DESPUES CONTROLADORES")
#app.register_blueprint(tabla_bp)

@app.route("/")
def home():

    print("ENTRO A HOME")

    return "HOME OK"

#print(app.url_map)


@app.route('/health')
def health():
    print("ENTRO A HEALTH")
    return "HEALTH OK"

@app.before_request
def debug_request():
    print("PETICION RECIBIDA")

print("APP CARGADA COMPLETAMENTE")
# =========================
# EJECUTAR APP
# =========================

@app.errorhandler(Exception)
def capturar_error(error):
    import traceback
    print(traceback.format_exc())
    return str(error), 500

print("FIN APP")

if __name__ == '__main__':

    app.run()
