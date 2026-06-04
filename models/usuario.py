from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)

    correo = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))

    rol = db.relationship('Rol')

    grupo = db.relationship('Grupo')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)