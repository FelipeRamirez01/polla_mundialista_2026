from flask import Flask

from extensions import db, login_manager

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================

app.config['SECRET_KEY'] = 'clave_super_segura'

#app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:utWabMlSivSEEkcYhNNfjtCTdDiXyVNN@acela.proxy.rlwy.net:25475/railway')
app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://konectan_pipe:Pipejulian1@207.210.102.204:3306/konectan_polla')
import os
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv( 'DATABASE_URL')

#app.config['SQLALCHEMY_DATABASE_URI'] = ('mysql+pymysql://root:root@localhost:3306/polla_mundial')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['APPLICATION_ROOT'] = '/polla_mundial'

# =========================
# INICIALIZAR EXTENSIONS
# =========================


db.init_app(app)



login_manager.init_app(app)

login_manager.login_view = 'login'


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


from controllers.admin_controller import *
from controllers.auth_controller import *
from controllers.grupo_controller import *
from controllers.partido_controller import *
from controllers.prediccion_controller import *
from controllers.usuario_controller import *
from controllers.tabla_controller import *
from controllers.usuario_controller import *

#app.register_blueprint(tabla_bp)



# =========================
# EJECUTAR APP
# =========================

@app.errorhandler(Exception)
def capturar_error(error):
    import traceback
    print(traceback.format_exc())
    return str(error), 500


if __name__ == '__main__':

    app.run()
