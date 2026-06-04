
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from sqlalchemy import func
from app import app
from extensions import db

from models.usuario import Usuario
from models.prediccion import Prediccion


##tabla_bp = Blueprint('tabla', __name__)

@app.route('/usuario/tabla-posiciones')
@login_required
def tabla_posiciones():

    tabla = db.session.query(
        Usuario.id,
        Usuario.nombre,
        func.coalesce(
            func.sum(Prediccion.puntos), 0
        ).label('total_puntos')
    ).outerjoin(
        Prediccion,
        Prediccion.usuario_id == Usuario.id
    ).filter(
        Usuario.grupo_id == current_user.grupo_id
    ).group_by(
        Usuario.id,
        Usuario.nombre
    ).order_by(
        func.coalesce(
            func.sum(Prediccion.puntos), 0
        ).desc()
    ).all()

    return render_template(
        'tabla/tabla_posiciones.html',
        tabla=tabla,
        grupo=current_user.grupo.nombre
    )