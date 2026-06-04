from extensions import db

class LlaveFifa2026(db.Model):

    __tablename__ = 'llaves_fifa_2026'

    id = db.Column(db.Integer, primary_key=True)

    ronda = db.Column(db.String(50))

    numero_partido = db.Column(db.Integer)

    posicion_local = db.Column(db.String(20))

    posicion_visitante = db.Column(db.String(20))

    siguiente_partido = db.Column(db.Integer)