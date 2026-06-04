from extensions import db


class TablaPosiciones(db.Model):

    __tablename__ = 'tabla_posiciones'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id'),
        nullable=False
    )

    grupo_id = db.Column(
        db.Integer,
        db.ForeignKey('grupos.id'),
        nullable=False
    )

    puntos = db.Column(
        db.Integer,
        default=0
    )

    partidos_acertados = db.Column(
        db.Integer,
        default=0
    )

    marcadores_exactos = db.Column(
        db.Integer,
        default=0
    )

    posicion = db.Column(
        db.Integer,
        default=0
    )

    usuario = db.relationship(
        'Usuario',
        backref='tabla_posiciones'
    )

    grupo = db.relationship(
        'Grupo',
        backref='tabla_posiciones'
    )