import requests

from extensions import db

from models.partido import Partido


API_KEY = 'TU_API_KEY'


def actualizar_resultados():

    url = 'https://v3.football.api-sports.io/fixtures'

    headers = {
        'x-apisports-key': API_KEY
    }

    response = requests.get(url, headers=headers)

    data = response.json()

    for item in data['response']:

        local = item['teams']['home']['name']
        visita = item['teams']['away']['name']

        goles_local = item['goals']['home']
        goles_visita = item['goals']['away']

        estado = item['fixture']['status']['short']

        partido = Partido.query.filter_by(
            equipo_local=local,
            equipo_visitante=visita
        ).first()

        if partido:

            partido.goles_local = goles_local
            partido.goles_visitante = goles_visita

            if estado == 'FT':
                partido.estado = 'Finalizado'

    db.session.commit()