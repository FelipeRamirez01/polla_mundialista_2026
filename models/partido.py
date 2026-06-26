from extensions import db

class Partido(db.Model):

    __tablename__ = 'partidos'

    id = db.Column(db.Integer, primary_key=True)

    fase = db.Column(db.String(50))

    grupo = db.Column(db.String(5))

    numero_partido = db.Column(db.Integer)

    equipo_local = db.Column(db.String(100))

    equipo_visitante = db.Column(db.String(100))

    goles_local = db.Column(db.Integer)

    goles_visitante = db.Column(db.Integer)

    fecha = db.Column(db.DateTime)

    ganador = db.Column(db.String(100))

    finalizado = db.Column(db.Boolean, default=False)