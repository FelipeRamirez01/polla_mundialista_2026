from app import app
from extensions import db
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from models.usuario import Usuario
from models.rol import Rol
from models.grupo import Grupo

# LOGIN
#@app.route('/')
#def home():
 #   return 'Funcionando'

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        correo = request.form['correo']
        password = request.form['password']

        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario and usuario.check_password(password):

            login_user(usuario)

            # REDIRECCIÓN SEGÚN EL ROL
            if usuario.rol.nombre == 'Administrador':
                return redirect(url_for('dashboard_admin'))

            elif usuario.rol.nombre == 'Usuario':
                return redirect(url_for('vista_usuario'))

            else:
                flash('Rol no válido')
                return redirect(url_for('login'))

        flash('Credenciales incorrectas')

    return render_template('login.html')

# REGISTRO
@app.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        codigo = request.form['codigo']

        grupo = Grupo.query.filter_by(codigo=codigo).first()

        if not grupo:
            flash('Código de grupo inválido')
            return redirect(url_for('registro'))

        rol_usuario = Rol.query.filter_by(nombre='Usuario').first()

        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            rol_id=rol_usuario.id,
            grupo_id=grupo.id
        )

        nuevo_usuario.set_password(password)

        db.session.add(nuevo_usuario)
        db.session.commit()

        flash('Usuario registrado correctamente')

        return redirect(url_for('login'))

    return render_template('registro.html')


# DASHBOARD ADMIN
@app.route('/dashboard-admin')
@login_required
def dashboard_admin():
    return render_template('admin/dashboard.html')

# DASHBOARD USUARIO
@app.route('/usuario')
@login_required
def vista_usuario():
    return render_template('usuario/index.html')


# LOGOUT
@app.route('/logout')
@login_required
def logout():

    logout_user()

    return redirect(url_for('login'))