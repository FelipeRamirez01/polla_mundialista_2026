from flask import flash, redirect, render_template, request, send_file, url_for
from flask_login import login_required, current_user
from app import app
from extensions import db
from models.partido import Partido
from models.prediccion import Prediccion


@app.route('/usuario/prediccion')
@login_required
def vista_usuario1():
    partidos = Partido.query.all()

    predicciones_usuario = Prediccion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    return render_template(
        'usuario/index.html',
        partidos=partidos,
        predicciones=predicciones_usuario
    )


@app.route('/guia-pdf')
@login_required
def descargar_guia_pdf():

    return send_file(
        'static/guia_polla_mundial_2026.pdf',
        as_attachment=True
    )



from string import ascii_uppercase

@app.route('/usuario/prediccioness')
@login_required
def prediccioness():

    grupos_validos = list(ascii_uppercase[:12])  # A hasta L

    partidos = Partido.query.filter(
        Partido.grupo.in_(grupos_validos)
    ).order_by(
        Partido.grupo.asc(),
        Partido.fecha.asc()
    ).all()

    grupos = {}

    for grupo in grupos_validos:

        grupos[grupo] = []

    for partido in partidos:

        if partido.grupo in grupos:
            grupos[partido.grupo].append(partido)

    return render_template(

        'usuario/predicciones.html',

        grupos=grupos
    )


@app.route('/guardar-predicciones', methods=['POST'])
@login_required
def guardar_predicciones():

    partidos = Partido.query.all()

    for partido in partidos:

        goles_local = request.form.get(f'local_{partido.id}')

        goles_visitante = request.form.get(f'visitante_{partido.id}')

        prediccion = Prediccion.query.filter_by(

            usuario_id=current_user.id,

            partido_id=partido.id

        ).first()

        if not prediccion:

            prediccion = Prediccion(

                usuario_id=current_user.id,

                partido_id=partido.id,

                goles_local=int(goles_local),

                goles_visitante=int(goles_visitante)

            )

            db.session.add(prediccion)

        else:

            prediccion.goles_local = int(goles_local)

            prediccion.goles_visitante = int(goles_visitante)

    db.session.commit()

    flash('Predicciones guardadas correctamente')

    return redirect(url_for('predicciones'))