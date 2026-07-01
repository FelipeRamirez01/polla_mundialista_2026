
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app import app
from extensions import db

from models.usuario import Usuario
from models.prediccion import Prediccion
from models.partido_eliminacion import PartidoEliminacion


##tabla_bp = Blueprint('tabla', __name__)

@app.route('/usuario/tabla-posiciones')
@login_required
def tabla_posiciones():

    # Puntos fase de grupos
    puntos_grupos = (
        db.session.query(
            Prediccion.usuario_id,
            func.coalesce(
                func.sum(Prediccion.puntos),
                0
            ).label("puntos_grupos")
        )
        .group_by(Prediccion.usuario_id)
        .subquery()
    )

    # Puntos por resultados de eliminación
    puntos_eliminacion = (
        db.session.query(
            PartidoEliminacion.usuario_id,
            func.coalesce(
                func.sum(PartidoEliminacion.puntos),
                0
            ).label("puntos_eliminacion")
        )
        .group_by(PartidoEliminacion.usuario_id)
        .subquery()
    )

    # Puntos por clasificación
    puntos_clasificacion = (
        db.session.query(
            PartidoEliminacion.usuario_id,
            func.coalesce(
                func.sum(PartidoEliminacion.puntos_clasificacion),
                0
            ).label("puntos_clasificacion")
        )
        .group_by(PartidoEliminacion.usuario_id)
        .subquery()
    )

    tabla = (
        db.session.query(

            Usuario.id,
            Usuario.nombre,

            func.coalesce(
                puntos_grupos.c.puntos_grupos,
                0
            ).label("puntos_grupos"),

            func.coalesce(
                puntos_eliminacion.c.puntos_eliminacion,
                0
            ).label("puntos_eliminacion"),

            func.coalesce(
                puntos_clasificacion.c.puntos_clasificacion,
                0
            ).label("puntos_clasificacion"),

            (
                func.coalesce(
                    puntos_grupos.c.puntos_grupos,
                    0
                )
                +
                func.coalesce(
                    puntos_eliminacion.c.puntos_eliminacion,
                    0
                )
                +
                func.coalesce(
                    puntos_clasificacion.c.puntos_clasificacion,
                    0
                )
            ).label("total_puntos")

        )
        .outerjoin(
            puntos_grupos,
            Usuario.id == puntos_grupos.c.usuario_id
        )
        .outerjoin(
            puntos_eliminacion,
            Usuario.id == puntos_eliminacion.c.usuario_id
        )
        .outerjoin(
            puntos_clasificacion,
            Usuario.id == puntos_clasificacion.c.usuario_id
        )
        .filter(
            Usuario.grupo_id == current_user.grupo_id
        )
        .order_by(
            (
                func.coalesce(
                    puntos_grupos.c.puntos_grupos,
                    0
                )
                +
                func.coalesce(
                    puntos_eliminacion.c.puntos_eliminacion,
                    0
                )
                +
                func.coalesce(
                    puntos_clasificacion.c.puntos_clasificacion,
                    0
                )
            ).desc(),
            Usuario.nombre.asc()
        )
        .all()
    )

    return render_template(
        "tabla/tabla_posiciones.html",
        tabla=tabla,
        grupo=current_user.grupo.nombre
    )