from extensions import db

class EscenarioTercerosFifa(db.Model):

    __tablename__ = 'escenarios_terceros_fifa'

    id = db.Column(db.Integer, primary_key=True)

    combinacion = db.Column(db.String(50))

    posicion = db.Column(db.String(20))

    grupo_tercero = db.Column(db.String(1))