from extensions import db
from datetime import datetime
from zoneinfo import ZoneInfo

class PartidoEliminacion(db.Model):

    __tablename__ = 'partidos_eliminacion'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )

    fase = db.Column(db.String(50), nullable=False)

    numero_partido = db.Column(
        db.Integer,
        nullable=False
    )

    equipo_local = db.Column(
        db.String(100),
        nullable=False
    )

    equipo_visitante = db.Column(
        db.String(100),
        nullable=False
    )

    goles_local = db.Column(db.Integer)

    goles_visitante = db.Column(db.Integer)

    ganador = db.Column(db.String(100))

    perdedor = db.Column(db.String(100))

    partido_origen_local = db.Column(db.Integer)

    partido_origen_visitante = db.Column(db.Integer)

    es_oficial = db.Column(db.Boolean,default=False)

    fecha_registro = db.Column(
        db.DateTime,
        default=lambda: datetime.now(
            ZoneInfo("America/Bogota")
        ),
        
    )

    puntos = db.Column(
        db.Integer,
        default=0
    )

    puntos_clasificacion = db.Column(
        db.Integer,
        default=0
    )

    usuario = db.relationship(
        'Usuario',
        backref='partidos_eliminacion'
    )