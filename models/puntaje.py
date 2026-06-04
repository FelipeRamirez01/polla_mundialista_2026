from extensions import db


class Puntaje(db.Model):

    __tablename__ = 'puntajes'

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id')
    )

    puntos = db.Column(db.Integer, default=0)

    usuario = db.relationship('Usuario')