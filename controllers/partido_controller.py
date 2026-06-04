from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app import app, db

from models.partido import Partido


@app.route('/partidos')
@login_required
def partidos():

    lista = Partido.query.order_by(Partido.fecha.asc()).all()

    return render_template(
        'partidos/index.html',
        partidos=lista
    )


@app.route('/partidos/crear', methods=['GET', 'POST'])
@login_required
def crear_partido():

    if current_user.rol.nombre != 'Administrador':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':

        partido = Partido(
            equipo_local=request.form['equipo_local'],
            equipo_visitante=request.form['equipo_visitante'],
            fecha=request.form['fecha'],
            fase=request.form['fase']
        )

        db.session.add(partido)

        db.session.commit()

        flash('Partido creado')

        return redirect(url_for('partidos'))

    return render_template('partidos/crear.html')