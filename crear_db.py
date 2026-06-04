
from app import app
from extensions import db

# =========================
# IMPORTAR MODELOS
# =========================

from models.rol import Rol
from models.usuario import Usuario
from models.grupo import Grupo
from models.partido import Partido
from models.prediccion import Prediccion
from models.tabla_posiciones import TablaPosiciones


# =========================
# CREAR BASE DE DATOS
# =========================

with app.app_context():

    # Crear todas las tablas
    db.create_all()

    print('===================================')
    print('BASE DE DATOS CREADA CORRECTAMENTE')
    print('===================================')

    # =========================
    # CREAR ROLES
    # =========================

    rol_admin = Rol.query.filter_by(
        nombre='Administrador'
    ).first()

    if not rol_admin:

        rol_admin = Rol(
            nombre='Administrador'
        )

        db.session.add(rol_admin)

        print('Rol Administrador creado')


    rol_usuario = Rol.query.filter_by(
        nombre='Usuario'
    ).first()

    if not rol_usuario:

        rol_usuario = Rol(
            nombre='Usuario'
        )

        db.session.add(rol_usuario)

        print('Rol Usuario creado')

    db.session.commit()


    # =========================
    # CREAR GRUPO PRINCIPAL
    # =========================

    grupo = Grupo.query.filter_by(
        codigo='MUNDIAL2026'
    ).first()

    if not grupo:

        grupo = Grupo(
            nombre='Grupo Principal',
            codigo='MUNDIAL2026'
        )

        db.session.add(grupo)

        db.session.commit()

        print('Grupo principal creado')


    # =========================
    # CREAR USUARIO ADMIN
    # =========================

    admin = Usuario.query.filter_by(
        correo='usuario@usuario.com'
    ).first()

    if not admin:

        admin = Usuario(
            nombre='usuario',
            correo='usuario@usuario.com',
            id_rol=2,
            grupo_id=1
        )

        # CONTRASEÑA
        admin.set_password('123456')

        db.session.add(admin)

        db.session.commit()

        print('Administrador creado')


        # =========================
        # CREAR TABLA POSICIONES
        # =========================

        tabla = TablaPosiciones(
            usuario_id=admin.id,
            grupo_id=grupo.id,
            puntos=0,
            partidos_acertados=0,
            marcadores_exactos=0,
            posicion=1
        )

        db.session.add(tabla)

        db.session.commit()

        print('Tabla posiciones administrador creada')


    print('===================================')
    print('CONFIGURACIÓN FINALIZADA')
    print('===================================')

