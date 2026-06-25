from extensions import db

class ControlCalculo(db.Model):
    __tablename__ = 'control_calculos'

    id = db.Column(db.Integer, primary_key=True)

    fase = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    ejecutado = db.Column(
        db.Boolean,
        default=False
    )

    fecha_ejecucion = db.Column(
        db.DateTime
    )