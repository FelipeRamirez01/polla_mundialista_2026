
from app import app
from extensions import db
from models.partido import Partido

from datetime import datetime, timedelta


def crear_partidos_grupo(grupo, equipos, numero_inicio, fecha_inicio):

    partidos = []

    encuentros = [

        (0, 1),
        (2, 3),

        (0, 2),
        (1, 3),

        (0, 3),
        (1, 2)

    ]

    numero = numero_inicio

    for i, (local, visitante) in enumerate(encuentros):

        fecha_partido = fecha_inicio + timedelta(days=i)

        partido = Partido(

            fase='Grupos',

            grupo=grupo,

            numero_partido=numero,

            equipo_local=equipos[local],

            equipo_visitante=equipos[visitante],

            fecha=fecha_partido,

            finalizado=False

        )

        partidos.append(partido)

        numero += 1

    return partidos


with app.app_context():

    todos_partidos = []

    numero_partido = 1

    # ==========================================
    # GRUPOS MUNDIAL 2026
    # ==========================================

    grupos = {

        'A': ['México', 'Canadá', 'Costa Rica', 'Estados Unidos'],

        'B': ['Argentina', 'Brasil', 'Chile', 'Uruguay'],

        'C': ['Francia', 'España', 'Portugal', 'Marruecos'],

        'D': ['Alemania', 'Italia', 'Países Bajos', 'Croacia'],

        'E': ['Inglaterra', 'Bélgica', 'Suiza', 'Dinamarca'],

        'F': ['Japón', 'Corea del Sur', 'Australia', 'Irán'],

        'G': ['Colombia', 'Ecuador', 'Perú', 'Paraguay'],

        'H': ['Nigeria', 'Senegal', 'Camerún', 'Ghana'],

        'I': ['Polonia', 'Serbia', 'Austria', 'Suecia'],

        'J': ['Panamá', 'Honduras', 'Jamaica', 'El Salvador'],

        'K': ['Arabia Saudita', 'Qatar', 'Irak', 'Emiratos Árabes'],

        'L': ['Nueva Zelanda', 'Fiyi', 'Tahiti', 'Islas Salomón']

    }

    # ==========================================
    # FECHAS OFICIALES APROXIMADAS
    # ==========================================

    fecha_inicio_mundial = datetime(2026, 6, 11, 18, 0)

    incremento_grupo = 2

    for index, (grupo, equipos) in enumerate(grupos.items()):

        fecha_grupo = fecha_inicio_mundial + timedelta(days=index * incremento_grupo)

        partidos = crear_partidos_grupo(

            grupo=grupo,

            equipos=equipos,

            numero_inicio=numero_partido,

            fecha_inicio=fecha_grupo

        )

        todos_partidos.extend(partidos)

        numero_partido += 6

    # ==========================================
    # GUARDAR EN BASE DE DATOS
    # ==========================================

    db.session.add_all(todos_partidos)

    db.session.commit()

    print('✅ Todos los partidos de grupos fueron cargados correctamente')

