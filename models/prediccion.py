from extensions import db


class Prediccion(db.Model):

    __tablename__ = 'predicciones'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id')
    )

    partido_id = db.Column(
        db.Integer,
        db.ForeignKey('partidos.id')
    )

    ganador = db.Column(db.Integer)  # 1 para local, 2 para visitante, 0 para empate
    goles_local = db.Column(db.Integer)
    goles_visitante = db.Column(db.Integer)
    puntos = db.Column(db.Integer, default=0)

    partido = db.relationship('Partido')