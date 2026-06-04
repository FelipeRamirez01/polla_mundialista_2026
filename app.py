from flask import Flask

from extensions import db, login_manager

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================

app.config['SECRET_KEY'] = 'clave_super_segura'

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'mysql+pymysql://root:root@localhost/polla_mundial'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

from controllers.auth_controller import *
from controllers.admin_controller import *
from controllers.usuario_controller import *

from controllers.tabla_controller import *
from controllers.grupo_controller import *
from controllers.prediccion_controller import *

#app.register_blueprint(tabla_bp)




# =========================
# IMPORTAR SCHEDULER
# =========================

from scheduler import scheduler


# =========================
# EJECUTAR APP
# =========================

if __name__ == '__main__':

    app.run(debug=True)