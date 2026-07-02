from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from collections import defaultdict
from app import app, db

from models.partido import Partido
from models.prediccion import Prediccion
from models.puntaje import Puntaje
from models.partido_eliminacion import PartidoEliminacion
from models.usuario import Usuario

@app.route('/usuario/predicciones')
@login_required
def predicciones():

    grupos_validos = ['A','B','C','D','E','F','G','H','I','J','K','L']

    partidos = Partido.query.filter(
        Partido.grupo.in_(grupos_validos)
    ).all()

    predicciones_usuario = Prediccion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    predicciones_ids = [
        p.partido_id
        for p in predicciones_usuario
    ]

    grupos = {}

    for grupo in grupos_validos:

        grupos[grupo] = [
            p for p in partidos
            if p.grupo == grupo
        ]

    total_partidos = len(partidos)

    total_predicciones = len(predicciones_ids)

    grupos_completos = (
        total_partidos == total_predicciones
    )



    fases = [
        ("Dieciseisavos", 16, "dieciseisavos"),
        ("Octavos", 8, "octavos"),
        ("Cuartos", 4, "cuartos"),
        ("Semifinal", 2, "semifinales"),
        ("Tercer Puesto", 1, "tercer_puesto"),
        ("Final", 1, "final_mundial"),
    ]

    siguiente = None

    for nombre, cantidad, ruta in fases:

        total = PartidoEliminacion.query.filter_by(
            usuario_id=current_user.id,
            fase=nombre
        ).count()

        print(f"Fase: {nombre}, Total: {total}, Cantidad: {cantidad}")

        

        if total < cantidad:

            siguiente = {
                "nombre": nombre,
                "ruta": ruta
            }

            break



    return render_template(

        'usuario/predicciones.html',

        grupos=grupos,

        partidos=partidos,

        predicciones_ids=predicciones_ids,

        grupos_completos=grupos_completos,

        siguiente=siguiente
    )


@app.route('/usuario/predicciones/guardar', methods=['POST'])
@login_required
def guardar_prediccion():

    partido_id = request.form['partido_id']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    # 1 = gana local
    # 2 = gana visitante
    # 0 = empate
    if goles_local > goles_visitante:
        ganador = 1
    elif goles_visitante > goles_local:
        ganador = 2
    else:
        ganador = 0

    existe = Prediccion.query.filter_by(
        usuario_id=current_user.id,
        partido_id=partido_id
    ).first()

    if existe:

        existe.goles_local = goles_local
        existe.goles_visitante = goles_visitante
        existe.ganador = ganador

    else:

        prediccion = Prediccion(
            usuario_id=current_user.id,
            partido_id=partido_id,
            goles_local=goles_local,
            goles_visitante=goles_visitante,
            ganador=ganador
        )

        db.session.add(prediccion)

    db.session.commit()

    flash('Predicción guardada correctamente', 'success')

    return redirect(url_for('predicciones'))

@app.route('/usuario/predicciones/guardar-grupo', methods=['POST'])
@login_required
def guardar_predicciones_grupo():

    grupo = request.form.get('grupo')

    partidos = Partido.query.filter_by(
        grupo=grupo
    ).all()

    for partido in partidos:

        goles_local = request.form.get(
            f'goles_local_{partido.id}'
        )

        goles_visitante = request.form.get(
            f'goles_visitante_{partido.id}'
        )

        if goles_local is None or goles_visitante is None:
            continue

        goles_local = int(goles_local)
        goles_visitante = int(goles_visitante)

        if goles_local > goles_visitante:
            ganador = 1

        elif goles_visitante > goles_local:
            ganador = 2

        else:
            ganador = 0

        existe = Prediccion.query.filter_by(
            usuario_id=current_user.id,
            partido_id=partido.id
        ).first()

        if existe:

            existe.goles_local = goles_local
            existe.goles_visitante = goles_visitante
            existe.ganador = ganador

        else:

            nueva = Prediccion(
                usuario_id=current_user.id,
                partido_id=partido.id,
                goles_local=goles_local,
                goles_visitante=goles_visitante,
                ganador=ganador
            )

            db.session.add(nueva)

    db.session.commit()

    flash(
        f'Predicciones del Grupo {grupo} guardadas correctamente',
        'success'
    )

    return redirect(
        url_for('predicciones')
    )


@app.route('/usuario/clasificacion_16')
@login_required
def clasificacion_16():

    grupos_validos = [
        'A', 'B', 'C', 'D',
        'E', 'F', 'G', 'H',
        'I', 'J', 'K', 'L'
    ]

    partidos = Partido.query.filter(
        Partido.grupo.in_(grupos_validos)
    ).all()

    predicciones = Prediccion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    predicciones_dict = {
        p.partido_id: p
        for p in predicciones
    }

    tablas = {}

    # CREAR TABLAS
    for grupo in grupos_validos:

        equipos = defaultdict(lambda: {
            'puntos': 0,
            'gf': 0,
            'gc': 0,
            'dg': 0
        })

        partidos_grupo = [
            p for p in partidos
            if p.grupo == grupo
        ]

        for partido in partidos_grupo:

            pred = predicciones_dict.get(partido.id)

            if not pred:
                continue

            local = partido.equipo_local
            visitante = partido.equipo_visitante

            gl = pred.goles_local
            gv = pred.goles_visitante

            equipos[local]['gf'] += gl
            equipos[local]['gc'] += gv

            equipos[visitante]['gf'] += gv
            equipos[visitante]['gc'] += gl

            if gl > gv:

                equipos[local]['puntos'] += 3

            elif gv > gl:

                equipos[visitante]['puntos'] += 3

            else:

                equipos[local]['puntos'] += 1
                equipos[visitante]['puntos'] += 1

        # DIFERENCIA GOL
        for equipo in equipos:

            equipos[equipo]['dg'] = (
                equipos[equipo]['gf']
                - equipos[equipo]['gc']
            )

        tabla_ordenada = sorted(

            equipos.items(),

            key=lambda x: (
                x[1]['puntos'],
                x[1]['dg'],
                x[1]['gf']
            ),

            reverse=True
        )

        tablas[grupo] = tabla_ordenada

    # CLASIFICADOS
    clasificados = {}

    for grupo, tabla in tablas.items():

        if len(tabla) >= 2:

            clasificados[grupo] = {
                'primero': tabla[0][0],
                'segundo': tabla[1][0]
            }


        tablas = calcular_tablas_usuario(
        current_user.id
    )

    terceros = []

    for grupo, tabla in tablas.items():

        if len(tabla) >= 3:

            terceros.append({

                'grupo': grupo,

                'equipo': tabla[2][0],

                'puntos': tabla[2][1]['puntos'],

                'dg': tabla[2][1]['dg'],

                'gf': tabla[2][1]['gf']

            })

    terceros = sorted(

        terceros,

        key=lambda x: (

            x['puntos'],
            x['dg'],
            x['gf']

        ),

        reverse=True

    )

    mejores_8 = terceros[:8]

    # CRUCES DIECISEISAVOS
    cruces = []

    grupos_lista = list(clasificados.keys())

    for i in range(0, len(grupos_lista), 2):

        if i + 1 < len(grupos_lista):

            grupo1 = grupos_lista[i]
            grupo2 = grupos_lista[i + 1]

            cruces.append({

                'partido': f'Dieciseisavo {i+1}',

                'local': clasificados[grupo1]['primero'],

                'visitante': clasificados[grupo2]['segundo']

            })

            cruces.append({

                'partido': f'Dieciseisavo {i+2}',

                'local': clasificados[grupo2]['primero'],

                'visitante': clasificados[grupo1]['segundo']

            })

    return render_template(

        'usuario/clasificacion_16.html',

        tablas=tablas,

        clasificados=clasificados,

        cruces=cruces,

        mejores_8=mejores_8,

        terceros=terceros
    )


from flask import render_template
from flask_login import login_required, current_user

def obtener_mejores_terceros(tablas):

    terceros = []

    for grupo, tabla in tablas.items():

        if len(tabla) < 3:
            continue

        terceros.append({

            "grupo": grupo,

            "equipo": tabla[2][0],

            "puntos": tabla[2][1]["puntos"],

            "dg": tabla[2][1]["dg"],

            "gf": tabla[2][1]["gf"]

        })

    terceros.sort(

        key=lambda x:(
            x["puntos"],
            x["dg"],
            x["gf"]
        ),

        reverse=True

    )

    return terceros

def obtener_mejores_8_terceros(usuario_id):

    terceros = obtener_mejores_terceros(usuario_id)

    return terceros[:8]

from collections import defaultdict
from models.partido import Partido
from models.prediccion import Prediccion

from collections import defaultdict

def calcular_tablas_usuario(usuario_id):

    grupos = ['A','B','C','D','E','F','G','H','I','J','K','L']

    # Todos los partidos
    partidos = Partido.query.filter(
        Partido.grupo.in_(grupos)
    ).all()

    # Todas las predicciones del usuario
    predicciones = Prediccion.query.filter_by(
        usuario_id=usuario_id
    ).all()

    predicciones_dict = {
        p.partido_id: p
        for p in predicciones
    }

    tablas = {}

    equipos_grupo = {
        g: defaultdict(lambda:{
            "puntos":0,
            "gf":0,
            "gc":0,
            "dg":0
        })
        for g in grupos
    }

    puntos_por_grupo = {g: 0 for g in grupos}

    for partido in partidos:

        pred = predicciones_dict.get(partido.id)

        if not pred:
            continue
        
        # Acumular puntos obtenidos en ese grupo
        puntos_por_grupo[partido.grupo] += pred.puntos

        equipos = equipos_grupo[partido.grupo]

        local = partido.equipo_local
        visita = partido.equipo_visitante

        gl = pred.goles_local
        gv = pred.goles_visitante

        equipos[local]["gf"] += gl
        equipos[local]["gc"] += gv

        equipos[visita]["gf"] += gv
        equipos[visita]["gc"] += gl

        if gl > gv:

            equipos[local]["puntos"] += 3

        elif gv > gl:

            equipos[visita]["puntos"] += 3

        else:

            equipos[local]["puntos"] += 1
            equipos[visita]["puntos"] += 1

    for grupo in grupos:

        for equipo in equipos_grupo[grupo]:

            equipos_grupo[grupo][equipo]["dg"] = (
                equipos_grupo[grupo][equipo]["gf"]
                -
                equipos_grupo[grupo][equipo]["gc"]
            )

        tablas[grupo] = sorted(

            equipos_grupo[grupo].items(),

            key=lambda x:(
                x[1]["puntos"],
                x[1]["dg"],
                x[1]["gf"]
            ),

            reverse=True

        )

    return tablas, puntos_por_grupo



@app.route('/usuario/mejores_terceros')
@login_required
def mejores_terceros():

    tablas = calcular_tablas_usuario(
        current_user.id
    )

    terceros = []

    for grupo, tabla in tablas.items():

        if len(tabla) >= 3:

            terceros.append({

                'grupo': grupo,

                'equipo': tabla[2][0],

                'puntos': tabla[2][1]['puntos'],

                'dg': tabla[2][1]['dg'],

                'gf': tabla[2][1]['gf']

            })

    terceros = sorted(

        terceros,

        key=lambda x: (

            x['puntos'],
            x['dg'],
            x['gf']

        ),

        reverse=True

    )

    mejores_8 = terceros[:8]

    return render_template(

        'usuario/mejores_terceros.html',

        terceros=terceros,

        mejores_8=mejores_8

    )


def obtener_clasificados(usuario_id):

    tablas = calcular_tablas_usuario(usuario_id)

    clasificados = {}

    for grupo, tabla in tablas.items():

        if len(tabla) >= 2:

            clasificados[f'1{grupo}'] = tabla[0][0]

            clasificados[f'2{grupo}'] = tabla[1][0]

    return clasificados

def obtener_mejores_terceros_dict(usuario_id):

    tablas = calcular_tablas_usuario(usuario_id)

    terceros = []

    for grupo, tabla in tablas.items():

        if len(tabla) >= 3:

            terceros.append({

                'grupo': grupo,

                'equipo': tabla[2][0],

                'puntos': tabla[2][1]['puntos'],

                'dg': tabla[2][1]['dg'],

                'gf': tabla[2][1]['gf']

            })

    terceros = sorted(

        terceros,

        key=lambda x: (

            x['puntos'],
            x['dg'],
            x['gf']

        ),

        reverse=True

    )

    mejores_8 = terceros[:8]

    resultado = {}

    for tercero in mejores_8:

        resultado[f"3{tercero['grupo']}"] = tercero['equipo']

    return resultado


def obtener_tercero(terceros, grupos_posibles):

    for grupo in grupos_posibles:

        clave = f'3{grupo}'

        if clave in terceros:

            equipo = terceros[clave]

            # Eliminar para que no vuelva a utilizarse
            del terceros[clave]

            return equipo

    return "POR DEFINIR"

@app.route('/usuario/dieciseisavos')
@login_required
def dieciseisavos():



    clasificados = obtener_clasificados(
        current_user.id
    )

    terceros = obtener_mejores_terceros_dict(
        current_user.id
    )

    cruces = [

        {
            'numero': 73,
            'local': clasificados.get('2A', 'POR DEFINIR'),
            'visitante': clasificados.get('2B', 'POR DEFINIR')
        },

        {
            'numero': 74,
            'local': clasificados.get('1E', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['A','B','C','D','F']
            )
        },

        {
            'numero': 75,
            'local': clasificados.get('1F', 'POR DEFINIR'),
            'visitante': clasificados.get('2C', 'POR DEFINIR')
        },

        {
            'numero': 76,
            'local': clasificados.get('1C', 'POR DEFINIR'),
            'visitante': clasificados.get('2F', 'POR DEFINIR')
        },

        {
            'numero': 77,
            'local': clasificados.get('1I', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['C','D','F','G','H']
            )
        },

        {
            'numero': 78,
            'local': clasificados.get('2E', 'POR DEFINIR'),
            'visitante': clasificados.get('2I', 'POR DEFINIR')
        },

        {
            'numero': 79,
            'local': clasificados.get('1A', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['C','E','F','H','I']
            )
        },

        {
            'numero': 80,
            'local': clasificados.get('1L', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['E','H','I','J','K']
            )
        },

        {
            'numero': 81,
            'local': clasificados.get('1D', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['B','E','F','I','J']
            )
        },

        {
            'numero': 82,
            'local': clasificados.get('1G', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['A','E','H','I','J']
            )
        },

        {
            'numero': 83,
            'local': clasificados.get('2K', 'POR DEFINIR'),
            'visitante': clasificados.get('2L', 'POR DEFINIR')
        },

        {
            'numero': 84,
            'local': clasificados.get('1H', 'POR DEFINIR'),
            'visitante': clasificados.get('2J', 'POR DEFINIR')
        },

        {
            'numero': 85,
            'local': clasificados.get('1B', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['E','F','G','I','J']
            )
        },

        {
            'numero': 86,
            'local': clasificados.get('1J', 'POR DEFINIR'),
            'visitante': clasificados.get('2H', 'POR DEFINIR')
        },

        {
            'numero': 87,
            'local': clasificados.get('1K', 'POR DEFINIR'),
            'visitante': obtener_tercero(
                terceros,
                ['D','E','I','J','L']
            )
        },

        {
            'numero': 88,
            'local': clasificados.get('2D', 'POR DEFINIR'),
            'visitante': clasificados.get('2G', 'POR DEFINIR')
        }

    ]

    partidos_guardados = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='DIECISEISAVOS'
    ).all()

    guardados = [
        p.numero_partido
        for p in partidos_guardados
    ]

    return render_template(

        'usuario/dieciseisavos.html',

        cruces=cruces,
        guardados=guardados

    )


from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user

@app.route('/usuario/guardar_dieciseisavos', methods=['POST'])
@login_required
def guardar_dieciseisavos():

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:

        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:

        ganador = equipo_visitante
        perdedor = equipo_local

    else:

        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':

            ganador = equipo_local
            perdedor = equipo_visitante

        else:

            ganador = equipo_visitante
            perdedor = equipo_local



    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Dieciseisavos',

        numero_partido=request.form['numero_partido'],

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],
        ganador=ganador,
        perdedor=perdedor,

        goles_local=goles_local,

        goles_visitante=goles_visitante

    )

    db.session.add(partido)
    db.session.commit()

    flash('Clasificado guardado correctamente')

    return redirect(url_for('dieciseisavos'))

@app.route('/usuario/octavos')
@login_required
def octavos():

    partidos_16 = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='Dieciseisavos'
    ).all()

    ganadores = {}

    for partido in partidos_16:
        ganadores[partido.numero_partido] = partido.ganador

    cruces = [

        {
            'numero': 89,
            'local': ganadores.get(74, 'POR DEFINIR'),
            'visitante': ganadores.get(77, 'POR DEFINIR')
        },

        {
            'numero': 90,
            'local': ganadores.get(73, 'POR DEFINIR'),
            'visitante': ganadores.get(75, 'POR DEFINIR')
        },

        {
            'numero': 91,
            'local': ganadores.get(76, 'POR DEFINIR'),
            'visitante': ganadores.get(78, 'POR DEFINIR')
        },

        {
            'numero': 92,
            'local': ganadores.get(79, 'POR DEFINIR'),
            'visitante': ganadores.get(80, 'POR DEFINIR')
        },

        {
            'numero': 93,
            'local': ganadores.get(83, 'POR DEFINIR'),
            'visitante': ganadores.get(84, 'POR DEFINIR')
        },

        {
            'numero': 94,
            'local': ganadores.get(81, 'POR DEFINIR'),
            'visitante': ganadores.get(82, 'POR DEFINIR')
        },

        {
            'numero': 95,
            'local': ganadores.get(86, 'POR DEFINIR'),
            'visitante': ganadores.get(88, 'POR DEFINIR')
        },

        {
            'numero': 96,
            'local': ganadores.get(85, 'POR DEFINIR'),
            'visitante': ganadores.get(87, 'POR DEFINIR')
        }

    ]

    partidos_guardados = PartidoEliminacion.query.filter_by(
    usuario_id=current_user.id,
    fase='OCTAVOS'
    ).all()

    guardados = [
        p.numero_partido
        for p in partidos_guardados
    ]

    return render_template(
        'usuario/octavos.html',
        cruces=cruces,
        guardados=guardados
    )


@app.route('/usuario/guardar_octavos', methods=['POST'])
@login_required
def guardar_octavos():

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:
        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:
            ganador = equipo_visitante
            perdedor = equipo_local

    else:
        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':
            ganador = equipo_local
            perdedor = equipo_visitante
        else:
            ganador = equipo_visitante
            perdedor = equipo_local


    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Octavos',

        numero_partido=request.form['numero_partido'],

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],

        ganador=ganador,   
        perdedor=perdedor,
        goles_local=goles_local,

        goles_visitante=goles_visitante

    )

    db.session.add(partido)
    db.session.commit()

    flash('Clasificado guardado correctamente')

    return redirect(url_for('octavos'))



@app.route('/usuario/cuartos')
@login_required
def cuartos():

    partidos_octavos = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='Octavos'
    ).all()

    ganadores = {}

    for partido in partidos_octavos:

        ganadores[partido.numero_partido] = partido.ganador

    cruces = [

        {
            'numero': 97,
            'local': ganadores.get(89, 'POR DEFINIR'),
            'visitante': ganadores.get(90, 'POR DEFINIR')
        },

        {
            'numero': 98,
            'local': ganadores.get(93, 'POR DEFINIR'),
            'visitante': ganadores.get(94, 'POR DEFINIR')
        },

        {
            'numero': 99,
            'local': ganadores.get(91, 'POR DEFINIR'),
            'visitante': ganadores.get(92, 'POR DEFINIR')
        },

        {
            'numero': 100,
            'local': ganadores.get(95, 'POR DEFINIR'),
            'visitante': ganadores.get(96, 'POR DEFINIR')
        }

    ]

    partidos_guardados = PartidoEliminacion.query.filter_by(
    usuario_id=current_user.id,
    fase='CUARTOS'
    ).all()

    guardados = [
        p.numero_partido
        for p in partidos_guardados
    ]

    return render_template(
        'usuario/cuartos.html',
        cruces=cruces,
        guardados=guardados
    )

@app.route('/usuario/guardar_cuartos', methods=['POST'])
@login_required
def guardar_cuartos():

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:
        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:
            ganador = equipo_visitante
            perdedor = equipo_local

    else:
        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':
            ganador = equipo_local
            perdedor = equipo_visitante
        else:
            ganador = equipo_visitante
            perdedor = equipo_local



    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Cuartos',

        numero_partido=request.form['numero_partido'],

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],
        ganador=ganador,

        perdedor=perdedor,

        goles_local=goles_local,

        goles_visitante=goles_visitante

    )

    db.session.add(partido)
    db.session.commit()

    flash('Clasificado guardado correctamente')

    return redirect(url_for('cuartos'))



@app.route('/usuario/semifinales')
@login_required
def semifinales():

    partidos_cuartos = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='Cuartos'
    ).all()

    ganadores = {}

    for partido in partidos_cuartos:

        ganadores[partido.numero_partido] = partido.ganador

    cruces = [

        {
            'numero': 101,
            'local': ganadores.get(97, 'POR DEFINIR'),
            'visitante': ganadores.get(98, 'POR DEFINIR')
        },

        {
            'numero': 102,
            'local': ganadores.get(99, 'POR DEFINIR'),
            'visitante': ganadores.get(100, 'POR DEFINIR')
        }

    ]

    partidos_guardados = PartidoEliminacion.query.filter_by(
    usuario_id=current_user.id,
    fase='SEMIFINAL'
    ).all()

    guardados = [
        p.numero_partido
        for p in partidos_guardados
    ]

    return render_template(
        'usuario/semifinales.html',
        cruces=cruces,
        guardados=guardados
    )

@app.route('/usuario/guardar_semifinales', methods=['POST'])
@login_required
def guardar_semifinales():


    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:
        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:
            ganador = equipo_visitante
            perdedor = equipo_local

    else:
        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':
            ganador = equipo_local
            perdedor = equipo_visitante
        else:
            ganador = equipo_visitante
            perdedor = equipo_local

    
    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Semifinal',

        numero_partido=request.form['numero_partido'],

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],
        ganador=ganador,
        perdedor=perdedor,

        goles_local=goles_local,

        goles_visitante=goles_visitante,

    )

    db.session.add(partido)
    db.session.commit()

    flash('Clasificado guardado correctamente')

    return redirect(url_for('semifinales'))


@app.route('/usuario/tercer_puesto')
@login_required
def tercer_puesto():

    semifinales = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='Semifinal'
    ).all()

    perdedores = {}

    for partido in semifinales:

        perdedores[partido.numero_partido] = partido.perdedor

    partido = {

        'numero': 103,

        'local': perdedores.get(101, 'POR DEFINIR'),

        'visitante': perdedores.get(102, 'POR DEFINIR')

    }

    partidos_guardados = PartidoEliminacion.query.filter_by(
    usuario_id=current_user.id,
    fase='TERCER PUESTO'
    ).all()

    guardados = [
        p.numero_partido
        for p in partidos_guardados
    ]

    return render_template(

        'usuario/tercer_puesto.html',

        partido=partido,
        guardados=guardados

    )

@app.route('/usuario/guardar_tercer_puesto', methods=['POST'])
@login_required
def guardar_tercer_puesto():

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:
        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:
            ganador = equipo_visitante
            perdedor = equipo_local

    else:
        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':
            ganador = equipo_local
            perdedor = equipo_visitante
        else:
            ganador = equipo_visitante
            perdedor = equipo_local    
        
    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Tercer Puesto',

        numero_partido=103,

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],
        ganador=ganador,
        perdedor=perdedor,

        goles_local=goles_local,

        goles_visitante=goles_visitante

    )

    db.session.add(partido)
    db.session.commit()

    flash('Resultado guardado correctamente')

    return redirect(url_for('tercer_puesto'))

@app.route('/usuario/final_mundial')
@login_required
def final_mundial():

    semifinales = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase='Semifinal'
    ).all()

    ganadores = {}

    for partido in semifinales:

        ganadores[partido.numero_partido] = partido.ganador

    final = {

        'numero': 104,

        'local': ganadores.get(101, 'POR DEFINIR'),

        'visitante': ganadores.get(102, 'POR DEFINIR')

    }

    return render_template(

        'usuario/final.html',

        final=final

    )

@app.route('/usuario/guardar_final', methods=['POST'])
@login_required
def guardar_final():

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    if goles_local > goles_visitante:
        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:
            ganador = equipo_visitante
            perdedor = equipo_local

    else:
        ganador_penales = request.form['ganador_penales']

        if ganador_penales == 'local':
            ganador = equipo_local
            perdedor = equipo_visitante
        else:
            ganador = equipo_visitante
            perdedor = equipo_local    

    partido = PartidoEliminacion(

        usuario_id=current_user.id,

        fase='Final',

        numero_partido=104,

        equipo_local=request.form['equipo_local'],

        equipo_visitante=request.form['equipo_visitante'],
        ganador=ganador,
        perdedor=perdedor,

        goles_local=goles_local,

        goles_visitante=goles_visitante

     )

    db.session.add(partido)
    db.session.commit()

    flash('Campeón registrado correctamente')

    return redirect(url_for('bracket'))


@app.route('/usuario/bracket')
@login_required
def bracket():
    usuario = Usuario.query.get_or_404(current_user.id)
    orden_grupos = [
        'A','B','C','D','E','F',
        'G','H','I','J','K','L'
    ]

    grupos = {}

    for letra in orden_grupos:

        grupos[letra] = Partido.query.filter_by(
            grupo=letra
        ).order_by(
            Partido.fecha.asc()
        ).all()

    predicciones = Prediccion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    predicciones_dict = {}

    for pred in predicciones:

        predicciones_dict[pred.partido_id] = pred

    tablas = calcular_tablas_usuario(
        current_user.id
    )


    

    mejores_terceros = obtener_mejores_8_terceros(
        current_user.id
    )

    eliminacion = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id
    ).all()

    datos = {}

    for partido in eliminacion:

        datos[partido.numero_partido] = partido



    return render_template(

        'usuario/bracket.html',
        usuario=usuario,

        grupos=grupos,

        tablas=tablas,

        mejores_terceros=mejores_terceros,

        predicciones_dict=predicciones_dict,

        datos=datos

    )

@app.route('/usuario/bracket/<int:usuario_id>')
@login_required
def ver_bracket_usuario(usuario_id):

    usuario = Usuario.query.get_or_404(usuario_id)

    # Orden de grupos
    orden_grupos = [
        "A","B","C","D","E","F",
        "G","H","I","J","K","L"
    ]

    # ==========================
    # Todos los partidos de grupos
    # (1 sola consulta)
    # ==========================
    partidos = Partido.query.filter(
        Partido.grupo.in_(orden_grupos)
    ).order_by(
        Partido.grupo.asc(),
        Partido.fecha.asc()
    ).all()

    grupos = {g: [] for g in orden_grupos}

    for partido in partidos:
        grupos[partido.grupo].append(partido)

    # ==========================
    # Predicciones usuario
    # ==========================
    predicciones = Prediccion.query.filter_by(
        usuario_id=usuario_id
    ).all()

    predicciones_dict = {
        p.partido_id: p
        for p in predicciones
    }

    # ==========================
    # Eliminación usuario
    # ==========================
    eliminacion = PartidoEliminacion.query.filter_by(
        usuario_id=usuario_id
    ).all()

    datos = {
        p.numero_partido: p
        for p in eliminacion
    }

    # ==========================
    # Tablas calculadas
    # ==========================
    tablas, puntos_por_grupo = calcular_tablas_usuario(usuario_id)

    mejores_terceros = obtener_mejores_terceros(tablas)

    return render_template(

        "usuario/bracket.html",

        usuario=usuario,

        grupos=grupos,

        tablas=tablas,

        mejores_terceros=mejores_terceros,

        predicciones_dict=predicciones_dict,

        datos=datos,
        puntos_por_grupo=puntos_por_grupo

    )

from datetime import datetime, date
from zoneinfo import ZoneInfo

@app.route('/usuario/resultados-partidos')
@login_required
def resultados_partidos():

    grupo = request.args.get('grupo')
    fecha = request.args.get('fecha')

    hoy = datetime.now(
        ZoneInfo("America/Bogota")
    ).date()

    query = Partido.query

    if grupo:

        query = query.filter(
            Partido.grupo == grupo
        )

    if fecha:

        try:

            fecha_busqueda = datetime.strptime(
                fecha,
                '%Y-%m-%d'
            ).date()

            query = query.filter(
                db.func.date(Partido.fecha) == fecha_busqueda
            )

        except ValueError:

            query = query.filter(
                db.func.date(Partido.fecha) == hoy
            )

    else:

        query = query.filter(
            db.func.date(Partido.fecha) == hoy
        )

    partidos = query.order_by(
        Partido.grupo.asc(),
        Partido.fecha.asc()
    ).all()

    datos = []


    for partido in partidos:

        # Fase de grupos
        if partido.numero_partido <= 72:

            predicciones = db.session.query(
                Usuario.nombre.label("usuario"),
                Prediccion.goles_local,
                Prediccion.goles_visitante,
                Prediccion.puntos
            ).join(
                Usuario,
                Usuario.id == Prediccion.usuario_id
            ).filter(
                Prediccion.partido_id == partido.id
            ).order_by(
                Prediccion.puntos.desc(),
                Usuario.nombre.asc()
            ).all()

        # Fases eliminatorias
        else:

            predicciones = db.session.query(
                Usuario.nombre.label("usuario"),
                PartidoEliminacion.equipo_local,
                PartidoEliminacion.equipo_visitante,
                PartidoEliminacion.goles_local,
                PartidoEliminacion.goles_visitante,
                PartidoEliminacion.puntos
            ).join(
                Usuario,
                Usuario.id == PartidoEliminacion.usuario_id
            ).filter(
                PartidoEliminacion.numero_partido == partido.numero_partido
            ).order_by(
                PartidoEliminacion.puntos.desc(),
                Usuario.nombre.asc()
            ).all()

        total_3 = sum(1 for p in predicciones if p.puntos == 3)
        total_1 = sum(1 for p in predicciones if p.puntos == 1)
        total_0 = sum(1 for p in predicciones if p.puntos == 0)

        datos.append({
            "partido": partido,
            "predicciones": predicciones,
            "total_3": total_3,
            "total_1": total_1,
            "total_0": total_0
        })


    return render_template(
        'usuario/resultados_partidos.html',
        datos=datos,
        grupo=grupo,
        fecha=fecha,
        hoy=hoy
    )




def ahora_colombia():
    return datetime.now(
        ZoneInfo("America/Bogota")
    )

@app.route('/usuario/guardar_eliminatoria', methods=['POST'])
@login_required
def guardar_eliminatoria():


    fase = request.form['fase']

    numero_partido = request.form.get(
        'numero_partido'
    )

    equipo_local = request.form['equipo_local']
    equipo_visitante = request.form['equipo_visitante']

    goles_local = int(
        request.form['goles_local']
    )

    goles_visitante = int(
        request.form['goles_visitante']
    )

    # Determinar ganador

    if goles_local > goles_visitante:

        ganador = equipo_local
        perdedor = equipo_visitante

    elif goles_visitante > goles_local:

        ganador = equipo_visitante
        perdedor = equipo_local

    else:

        ganador_penales = request.form[
            'ganador_penales'
        ]

        if ganador_penales == 'local':

            ganador = equipo_local
            perdedor = equipo_visitante

        else:

            ganador = equipo_visitante
            perdedor = equipo_local

    existente = PartidoEliminacion.query.filter_by(
        usuario_id=current_user.id,
        fase=fase,
        numero_partido=numero_partido
    ).first()

    if existente:

        existente.equipo_local = equipo_local
        existente.equipo_visitante = equipo_visitante

        existente.goles_local = goles_local
        existente.goles_visitante = goles_visitante

        existente.ganador = ganador
        existente.perdedor = perdedor

    else:

        nuevo = PartidoEliminacion(

            usuario_id=current_user.id,

            fase=fase,

            numero_partido=numero_partido,

            equipo_local=equipo_local,

            equipo_visitante=equipo_visitante,

            goles_local=goles_local,

            goles_visitante=goles_visitante,

            ganador=ganador,
            fecha_registro=ahora_colombia(),

            perdedor=perdedor

        )

        db.session.add(nuevo)

    db.session.commit()

    flash(
        f'{fase} guardado correctamente',
        'success'
    )

    rutas = {
        'Dieciseisavos': 'dieciseisavos',
        'Octavos': 'octavos',
        'Cuartos': 'cuartos',
        'Semifinal': 'semifinales',
        'Tercer Puesto': 'tercer_puesto',
        'Final': 'bracket'
    }

    return redirect(
        url_for(rutas[fase])
    )




@app.route('/test_tablas')
def test_tablas():

    tablas = calcular_tablas_usuario(2)

    print(type(tablas))
    print(tablas)

    return str(tablas)

@app.route('/test_terceros')
def test_terceros():

    terceros = obtener_mejores_terceros(2)

    print(type(terceros))
    print(terceros)

    return str(terceros)
