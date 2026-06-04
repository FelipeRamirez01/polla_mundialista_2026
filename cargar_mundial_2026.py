from app import app
from extensions import db
from models.partido import Partido

from datetime import datetime


with app.app_context():

    partidos = []

    # =========================
    # FASE DE GRUPOS
    # =========================

    grupos = ['A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L']

    numero = 1

    for grupo in grupos:

        for i in range(1, 7):

            partido = Partido(

                fase='Grupos',

                grupo=grupo,

                numero_partido=numero,

                equipo_local=f'Selección {grupo}{i}',

                equipo_visitante=f'Selección {grupo}{i+1}',

                fecha=datetime(2026, 6, 10)

            )

            partidos.append(partido)

            numero += 1

    # =========================
    # DIECISEISAVOS
    # =========================

    for i in range(1, 17):

        partido = Partido(

            fase='Dieciseisavos',

            numero_partido=numero,

            equipo_local='Por definir',

            equipo_visitante='Por definir',

            fecha=datetime(2026, 7, 1)

        )

        partidos.append(partido)

        numero += 1

    # =========================
    # OCTAVOS
    # =========================

    for i in range(1, 9):

        partido = Partido(

            fase='Octavos',

            numero_partido=numero,

            equipo_local='Por definir',

            equipo_visitante='Por definir',

            fecha=datetime(2026, 7, 5)

        )

        partidos.append(partido)

        numero += 1

    # =========================
    # CUARTOS
    # =========================

    for i in range(1, 5):

        partido = Partido(

            fase='Cuartos',

            numero_partido=numero,

            equipo_local='Por definir',

            equipo_visitante='Por definir',

            fecha=datetime(2026, 7, 9)

        )

        partidos.append(partido)

        numero += 1

    # =========================
    # SEMIFINALES
    # =========================

    for i in range(1, 3):

        partido = Partido(

            fase='Semifinal',

            numero_partido=numero,

            equipo_local='Por definir',

            equipo_visitante='Por definir',

            fecha=datetime(2026, 7, 13)

        )

        partidos.append(partido)

        numero += 1

    # =========================
    # TERCER PUESTO
    # =========================

    tercer_puesto = Partido(

        fase='Tercer Puesto',

        numero_partido=numero,

        equipo_local='Por definir',

        equipo_visitante='Por definir',

        fecha=datetime(2026, 7, 18)

    )

    partidos.append(tercer_puesto)

    numero += 1

    # =========================
    # FINAL
    # =========================

    final = Partido(

        fase='Final',

        numero_partido=numero,

        equipo_local='Por definir',

        equipo_visitante='Por definir',

        fecha=datetime(2026, 7, 19)

    )

    partidos.append(final)

    # GUARDAR

    db.session.add_all(partidos)

    db.session.commit()

    print('✅ Mundial 2026 cargado correctamente')