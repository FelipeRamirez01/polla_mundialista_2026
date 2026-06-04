from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import app
from extensions import db

from models.usuario import Usuario
from models.rol import Rol
from models.grupo import Grupo
from models.prediccion import Prediccion
from models.partido import Partido


# VALIDAR ADMIN
def validar_admin():

    if current_user.rol.nombre != 'Administrador':
        return False

    return True


# =========================================
# LISTAR USUARIOS
# =========================================
@app.route('/admin/usuarios')
@login_required
def admin_usuarios():

    if not validar_admin():
        return redirect(url_for('dashboard'))

    usuarios = Usuario.query.all()

    return render_template(
        'admin/usuarios.html',
        usuarios=usuarios
    )


# =========================================
# CREAR USUARIO
# =========================================
@app.route('/admin/usuarios/crear', methods=['GET', 'POST'])
@login_required
def crear_usuario():

    if not validar_admin():
        return redirect(url_for('dashboard'))

    roles = Rol.query.all()

    grupos = Grupo.query.all()

    if request.method == 'POST':

        nombre = request.form['nombre']
        correo = request.form['correo']
        password = request.form['password']
        rol_id = request.form['rol_id']
        grupo_id = request.form['grupo_id']

        existe = Usuario.query.filter_by(correo=correo).first()

        if existe:
            flash('El correo ya existe')
            return redirect(url_for('crear_usuario'))

        usuario = Usuario(
            nombre=nombre,
            correo=correo,
            rol_id=rol_id,
            grupo_id=grupo_id
        )

        usuario.set_password(password)

        db.session.add(usuario)

        db.session.commit()

        flash('Usuario creado correctamente')

        return redirect(url_for('admin_usuarios'))

    return render_template(
        'admin/crear_usuario.html',
        roles=roles,
        grupos=grupos
    )


# =========================================
# EDITAR USUARIO
# =========================================
@app.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):

    if not validar_admin():
        return redirect(url_for('dashboard'))

    usuario = Usuario.query.get_or_404(id)

    roles = Rol.query.all()

    grupos = Grupo.query.all()

    if request.method == 'POST':

        usuario.nombre = request.form['nombre']
        usuario.correo = request.form['correo']
        usuario.rol_id = request.form['rol_id']
        usuario.grupo_id = request.form['grupo_id']

        password = request.form['password']

        if password != '':
            usuario.set_password(password)

        db.session.commit()

        flash('Usuario actualizado')

        return redirect(url_for('admin_usuarios'))

    return render_template(
        'admin/editar_usuario.html',
        usuario=usuario,
        roles=roles,
        grupos=grupos
    )


# =========================================
# ELIMINAR USUARIO
# =========================================
@app.route('/admin/usuarios/eliminar/<int:id>')
@login_required
def eliminar_usuario(id):

    if not validar_admin():
        return redirect(url_for('dashboard'))

    usuario = Usuario.query.get_or_404(id)

    db.session.delete(usuario)

    db.session.commit()

    flash('Usuario eliminado')

    return redirect(url_for('admin_usuarios'))


## FUNCION PARA CALCULAR PUNTOS DE UNA PREDICCION - FASE DE GRUPOS
def calcular_puntos(prediccion, partido):

    # Marcador exacto
    if (
        prediccion.goles_local == partido.goles_local
        and
        prediccion.goles_visitante == partido.goles_visitante
    ):
        return 3

    # Ganador real
    if partido.goles_local > partido.goles_visitante:
        ganador_real = 1

    elif partido.goles_local < partido.goles_visitante:
        ganador_real = 2

    else:
        ganador_real = 0

    # Ganador pronosticado
    if prediccion.goles_local > prediccion.goles_visitante:
        ganador_predicho = 1

    elif prediccion.goles_local < prediccion.goles_visitante:
        ganador_predicho = 2

    else:
        ganador_predicho = 0

    if ganador_real == ganador_predicho:
        return 1

    return 0


def actualizar_puntos_partido(partido_id):

    partido = Partido.query.get(partido_id)

    predicciones = Prediccion.query.filter_by(
        partido_id=partido_id
    ).all()

    for prediccion in predicciones:

        prediccion.puntos = calcular_puntos(
            prediccion,
            partido
        )

    db.session.commit()


@app.route('/admin/resultados')
@login_required
def admin_resultados():

    if current_user.rol.nombre != 'Administrador':
        flash('No tiene permisos para acceder.')
        return redirect(url_for('dashboard'))

    partidos = Partido.query.order_by(
        Partido.fecha.asc()
    ).all()

    return render_template(
        'admin/resultados.html',
        partidos=partidos
    )

@app.route('/admin/resultados/guardar', methods=['POST'])
@login_required
def guardar_resultado():

    if current_user.rol.nombre != 'Administrador':
        flash('No tiene permisos para acceder.')
        return redirect(url_for('dashboard'))

    partido = Partido.query.get_or_404(
        request.form['partido_id']
    )

    partido.goles_local = int(
        request.form['goles_local']
    )

    partido.goles_visitante = int(
        request.form['goles_visitante']
    )

    partido.finalizado = True

    db.session.commit()

    actualizar_puntos_partido(
        partido.id
    )

    flash(
        'Resultado actualizado correctamente',
        'success'
    )

    return redirect(
        url_for('admin_resultados')
    )




from sqlalchemy import func

@app.route('/admin/tabla-posiciones')
@login_required
def admin_tabla_posiciones():

    if current_user.rol.nombre != 'Administrador':
        flash('No tiene permisos para acceder.')
        return redirect(url_for('dashboard'))

    grupo_id = request.args.get('grupo_id', type=int)

    grupos = Grupo.query.order_by(
        Grupo.nombre
    ).all()

    tabla = []

    if grupo_id:

        tabla = db.session.query(
            Usuario.id,
            Usuario.nombre,
            Grupo.nombre.label('grupo'),
            func.coalesce(
                func.sum(Prediccion.puntos), 0
            ).label('total_puntos')
        ).join(
            Grupo,
            Usuario.grupo_id == Grupo.id
        ).outerjoin(
            Prediccion,
            Prediccion.usuario_id == Usuario.id
        ).filter(
            Usuario.grupo_id == grupo_id
        ).group_by(
            Usuario.id,
            Usuario.nombre,
            Grupo.nombre
        ).order_by(
            func.coalesce(
                func.sum(Prediccion.puntos), 0
            ).desc()
        ).all()

    return render_template(
        'admin/tabla_posiciones.html',
        grupos=grupos,
        tabla=tabla,
        grupo_id=grupo_id
    )