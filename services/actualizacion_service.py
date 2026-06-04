from extensions import db

from models.partido import Partido
from models.prediccion import Prediccion
from models.tabla_posiciones import TablaPosiciones


def calcular_puntajes():

    partidos = Partido.query.filter_by(finalizado=True).all()

    for partido in partidos:

        predicciones = Prediccion.query.filter_by(
            partido_id=partido.id
        ).all()

        for prediccion in predicciones:

            puntos = 0

            # RESULTADO REAL
            real_local = partido.goles_local
            real_visitante = partido.goles_visitante

            # RESULTADO USUARIO
            pred_local = prediccion.goles_local
            pred_visitante = prediccion.goles_visitante

            # ACIERTO EXACTO
            if (
                real_local == pred_local and
                real_visitante == pred_visitante
            ):

                puntos = 10

            else:

                # GANADOR REAL
                ganador_real = None

                if real_local > real_visitante:
                    ganador_real = 'LOCAL'

                elif real_visitante > real_local:
                    ganador_real = 'VISITANTE'

                else:
                    ganador_real = 'EMPATE'

                # GANADOR PREDICHO
                ganador_pred = None

                if pred_local > pred_visitante:
                    ganador_pred = 'LOCAL'

                elif pred_visitante > pred_local:
                    ganador_pred = 'VISITANTE'

                else:
                    ganador_pred = 'EMPATE'

                if ganador_real == ganador_pred:
                    puntos = 5

            prediccion.puntos = puntos

            # ACTUALIZAR TABLA
            tabla = TablaPosiciones.query.filter_by(
                usuario_id=prediccion.usuario_id
            ).first()

            if tabla:

                tabla.puntos += puntos

        db.session.commit()

    print('Puntajes actualizados')