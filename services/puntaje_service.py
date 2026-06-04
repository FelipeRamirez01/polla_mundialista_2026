from extensions import db

from models.partido import Partido
from models.prediccion import Prediccion
from models.puntaje import Puntaje


def calcular_puntajes():

    partidos = Partido.query.filter_by(estado='Finalizado').all()

    for partido in partidos:

        predicciones = Prediccion.query.filter_by(
            partido_id=partido.id
        ).all()

        for prediccion in predicciones:

            puntos = 0

            real_local = partido.goles_local
            real_visitante = partido.goles_visitante

            pred_local = prediccion.goles_local
            pred_visitante = prediccion.goles_visitante

            if (
                real_local == pred_local and
                real_visitante == pred_visitante
            ):
                puntos = 10

            else:

                ganador_real = None
                ganador_pred = None

                if real_local > real_visitante:
                    ganador_real = 'LOCAL'

                elif real_visitante > real_local:
                    ganador_real = 'VISITA'

                else:
                    ganador_real = 'EMPATE'

                if pred_local > pred_visitante:
                    ganador_pred = 'LOCAL'

                elif pred_visitante > pred_local:
                    ganador_pred = 'VISITA'

                else:
                    ganador_pred = 'EMPATE'

                if ganador_real == ganador_pred:
                    puntos = 5

            prediccion.puntos = puntos

            puntaje = Puntaje.query.filter_by(
                usuario_id=prediccion.usuario_id
            ).first()

            if not puntaje:

                puntaje = Puntaje(
                    usuario_id=prediccion.usuario_id,
                    puntos=0
                )

                db.session.add(puntaje)

            total = db.session.query(
                db.func.sum(Prediccion.puntos)
            ).filter_by(
                usuario_id=prediccion.usuario_id
            ).scalar()

            puntaje.puntos = total or 0

    db.session.commit()