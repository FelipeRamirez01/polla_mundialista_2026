from extensions import db

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

    usuario = db.relationship(
        'Usuario',
        backref='partidos_eliminacion'
    )