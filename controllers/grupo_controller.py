from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import app
from extensions import db

from models.grupo import Grupo


# =========================
# VER GRUPOS
# =========================
@app.route('/grupos')
@login_required
def grupos():

    grupos = Grupo.query.all()

    return render_template(
        'admin/grupos.html',
        grupos=grupos
    )


# =========================
# CREAR GRUPO
# =========================
@app.route('/crear-grupo', methods=['POST'])
@login_required
def crear_grupo():

    nombre = request.form['nombre']
    codigo = request.form['codigo']

    nuevo_grupo = Grupo(
        nombre=nombre,
        codigo=codigo
    )

    db.session.add(nuevo_grupo)
    db.session.commit()

    flash('Grupo creado correctamente', 'success')

    return redirect(url_for('grupos'))


# =========================
# EDITAR GRUPO
# =========================
@app.route('/editar-grupo/<int:id>', methods=['POST'])
@login_required
def editar_grupo(id):

    grupo = Grupo.query.get_or_404(id)

    grupo.nombre = request.form['nombre']
    grupo.codigo = request.form['codigo']

    db.session.commit()

    flash('Grupo actualizado correctamente', 'warning')

    return redirect(url_for('grupos'))


# =========================
# ELIMINAR GRUPO
# =========================
@app.route('/eliminar-grupo/<int:id>')
@login_required
def eliminar_grupo(id):

    grupo = Grupo.query.get_or_404(id)

    db.session.delete(grupo)
    db.session.commit()

    flash('Grupo eliminado correctamente', 'danger')

    return redirect(url_for('grupos'))

