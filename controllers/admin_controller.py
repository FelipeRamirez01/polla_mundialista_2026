from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from app import app
from extensions import db

from models.usuario import Usuario
from models.rol import Rol
from models.grupo import Grupo
from models.prediccion import Prediccion
from models.partido import Partido
from models.partido_eliminacion import PartidoEliminacion

from models.control_calculo import ControlCalculo
from datetime import datetime

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

    partido = Partido.query.get_or_404(partido_id)

    # ==========================================
    # FASE DE GRUPOS
    # ==========================================

    predicciones = Prediccion.query.filter_by(
        partido_id=partido_id
    ).all()

    for prediccion in predicciones:

        prediccion.puntos = calcular_puntos(
            prediccion,
            partido
        )

    # ==========================================
    # FASES ELIMINATORIAS
    # ==========================================

    if partido.numero_partido >= 73:  # Dieciseisavos o posteriores


        ganador_real = partido.ganador
        # Equipo ganador real
        if partido.goles_local > partido.goles_visitante:

            equipo_ganador_real = "Local"

        elif partido.goles_visitante > partido.goles_local:

            equipo_ganador_real = "Visitante"

        else:

            equipo_ganador_real = "Empate"   # Empate (definido por penales)

        predicciones_eliminacion = PartidoEliminacion.query.filter_by(
            numero_partido=partido.numero_partido
        ).all()

        for pred in predicciones_eliminacion:

            # Equipo ganador predicho
            if pred.goles_local > pred.goles_visitante:

                equipo_ganador_predicho = "Local"

            elif pred.goles_visitante > pred.goles_local:

                equipo_ganador_predicho = "Visitante"

            else:

                # Si el usuario predijo empate, debe escoger el ganador
                equipo_ganador_predicho = None

            # 3 puntos por marcador exacto 
            if (

                (
                    pred.goles_local == partido.goles_local
                    and
                    pred.goles_visitante == partido.goles_visitante
                )

            ):

                pred.puntos = 3

            # 1 punto por acertar el equipo ganador
            elif (
                equipo_ganador_real == equipo_ganador_predicho
            ):

                pred.puntos = 1

            else:

                pred.puntos = 0

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
        request.form['numero_partido']
    )

    partido.goles_local = int(
        request.form['goles_local']
    )

    partido.goles_visitante = int(
        request.form['goles_visitante']
    )

    partido.finalizado = True

    goles_local = int(request.form['goles_local'])
    goles_visitante = int(request.form['goles_visitante'])

    ganador = None

    if partido.numero_partido >= 73 and goles_local == goles_visitante:

        ganador = request.form.get('ganador')

    elif goles_local > goles_visitante:

        ganador = partido.equipo_local
    
    elif goles_local < goles_visitante:

        ganador = partido.equipo_visitante
    else:

        ganador = None

    partido.ganador = ganador
    
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
        return redirect(url_for('login'))

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

from datetime import datetime
from zoneinfo import ZoneInfo

def ahora_colombia():
    return datetime.now(
        ZoneInfo("America/Bogota")
    ).replace(tzinfo=None)

@app.route('/admin/panel-calculos')
@login_required
def panel_calculos():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(
            url_for('login')
        )
    
    calculos = {
        c.fase: c
        for c in ControlCalculo.query.all()
    }

    return render_template(
        'admin/panel_calculos.html',
        calculos=calculos
    )

def validar_clasificados_dieciseisavos():

    # Equipos reales que llegaron a Dieciseisavos
    partidos_reales = Partido.query.filter(
        Partido.numero_partido.between(73, 88)
    ).all()

    equipos_reales = set()

    for partido in partidos_reales:

        equipos_reales.add(
            partido.equipo_local
        )

        equipos_reales.add(
            partido.equipo_visitante
        )

    # Predicciones usuarios
    predicciones = PartidoEliminacion.query.filter(
        PartidoEliminacion.numero_partido.between(
            73,
            88
        )
    ).all()

    for prediccion in predicciones:

        puntos = 0

        if prediccion.equipo_local in equipos_reales:
            puntos += 5

        if prediccion.equipo_visitante in equipos_reales:
            puntos += 5

        prediccion.puntos = puntos

    db.session.commit()


def validar_clasificados_fase(numero_inicio, numero_fin, fase):

    puntajes = {
        "Dieciseisavos": 5,
        "Octavos": 8,
        "Cuartos": 10,
        "Semifinal": 12,
        "Final": 15,
        "Campeón": 20
    }

    puntos_fase = puntajes.get(fase, 5)

    partidos_reales = Partido.query.filter(
        Partido.numero_partido.between(
            numero_inicio,
            numero_fin
        )
    ).all()

    partidos_dict = {
        partido.numero_partido: partido
        for partido in partidos_reales
    }

    predicciones = PartidoEliminacion.query.filter_by(
        fase=fase
    ).all()

    for prediccion in predicciones:

        partido_real = partidos_dict.get(
            prediccion.numero_partido
        )

        puntos = 0

        if not partido_real:
            prediccion.puntos_clasificacion = 0
            continue

        # ===============================
        # CAMPEON
        # ===============================
        

        if ( fase == "Final"
            and
            prediccion.ganador
            and
            partido_real.ganador
            and
            prediccion.ganador == partido_real.ganador
            ):
                puntos += 20

        # ===============================
        # RESTO DE FASES
        # ===============================
        

        equipos_reales = {
            partido_real.equipo_local,
            partido_real.equipo_visitante
        }

        if prediccion.equipo_local in equipos_reales:
            puntos += puntos_fase

        if prediccion.equipo_visitante in equipos_reales:
            puntos += puntos_fase

        prediccion.puntos_clasificacion = puntos

    db.session.commit()
    



@app.route('/admin/validar-clasificados-dieciseisavos')
@login_required
def validar_clasificados_dieciseisavos_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))
    

    control = ControlCalculo.query.filter_by(
        fase='Dieciseisavos'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )

    validar_clasificados_fase(73,88,'Dieciseisavos')


    if not control:

        control = ControlCalculo(
            fase='Dieciseisavos'
        )

        db.session.add(control)

    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()


    flash(
        'Puntos por clasificados a Dieciseisavos actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )

@app.route('/admin/validar-clasificados-octavos')
@login_required
def validar_clasificados_octavos_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))
    
    control = ControlCalculo.query.filter_by(
        fase='Octavos'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )


    validar_clasificados_fase(89,96,'Octavos')

    if not control:

        control = ControlCalculo(
            fase='Octavos'
        )

        db.session.add(control)

    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()

    flash(
        'Puntos por clasificados a Octavos actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )


@app.route('/admin/validar-clasificados-cuartos')
@login_required
def validar_clasificados_cuartos_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))

    control = ControlCalculo.query.filter_by(
        fase='Cuartos'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )

    validar_clasificados_fase(97,100,'Cuartos')

    if not control:

        control = ControlCalculo(
            fase='Cuartos'
        )

        db.session.add(control)

    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()

    flash(
        'Puntos por clasificados a Cuartos actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )

@app.route('/admin/validar-clasificados-semis')
@login_required
def validar_clasificados_semis_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))

    control = ControlCalculo.query.filter_by(
        fase='Semifinal'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )

    validar_clasificados_fase(101,102,'Semifinal')

    if not control:

        control = ControlCalculo(
            fase='Semifinal'
        )

        db.session.add(control)

    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()

    flash(
        'Puntos por clasificados a Semis actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )


@app.route('/admin/validar-clasificados-tercer-puesto')
@login_required
def validar_clasificados_tercer_puesto_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))
    
    control = ControlCalculo.query.filter_by(
        fase='Tercer Puesto'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )


    validar_clasificados_fase(103,103,'Tercer Puesto')

    if not control:

        control = ControlCalculo(
            fase='Tercer Puesto'
        )

        db.session.add(control)

    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()

    flash(
        'Puntos por clasificados a Tercer Puesto actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )

@app.route('/admin/validar-clasificados-final')
@login_required
def validar_clasificados_final_admin():

    if current_user.rol.nombre != 'Administrador':

        flash(
            'No tiene permisos para acceder.',
            'danger'
        )

        return redirect(url_for('login'))

    control = ControlCalculo.query.filter_by(
        fase='Final'
    ).first()

    if control and control.ejecutado:

        flash(
            'Este cálculo ya fue ejecutado.',
            'warning'
        )

        return redirect(
            url_for('panel_calculos')
        )

    validar_clasificados_fase(104,104,'Final')

    if not control:

        control = ControlCalculo(
            fase='Final'
        )

        db.session.add(control)
    
    control.ejecutado = True
    control.fecha_ejecucion = ahora_colombia()

    db.session.commit()

    flash(
        'Puntos por clasificados a Final actualizados correctamente.',
        'success'
    )

    return redirect(
        url_for('panel_calculos')
    )

# DASHBOARD USUARIO
@app.route('/vista-finales')
@login_required
def vista_finales():
    return render_template('usuario/etapas_finales.html')


from collections import defaultdict
from flask import request, render_template, abort
from flask_login import login_required

@app.route('/validacion-clasificados/<fase>')
@login_required
def validacion_clasificados(fase):

    #if current_user.rol.nombre != "Administrador":
     #   abort(403)

    fases = {
        "Dieciseisavos": (73, 88),
        "Octavos": (89, 96),
        "Cuartos": (97, 100),
        "Semifinal": (101, 102),
        "Tercer Puesto": (103, 103),
        "Final": (104, 104),
        "Campeon": (104, 104)

    }

   

    if fase not in fases:
        abort(404)

    inicio, fin = fases[fase]

    puntajes = {
        "Dieciseisavos": 5,
        "Octavos": 8,
        "Cuartos": 10,
        "Semifinal": 12,
        "Final": 15,
        "Campeón": 20
    }

    puntos_fase = puntajes.get(fase, 5)

    grupo_filtro = "Amigos Mundial"  # request.args.get("grupo", None)

    # ============================
    # EQUIPOS REALES CLASIFICADOS
    # ============================

    partidos_reales = Partido.query.filter(
        Partido.numero_partido.between(inicio, fin)
    ).order_by(
        Partido.numero_partido
    ).all()


    # Diccionario para acceder al partido por número
    partidos_dict = {
        partido.numero_partido: partido
        for partido in partidos_reales
    }

    equipos_reales = set()

    for partido in partidos_reales:

        equipos_reales.add(partido.equipo_local)
        equipos_reales.add(partido.equipo_visitante)

    # ============================
    # USUARIOS
    # ============================

    usuarios_query = Usuario.query.join(
        Grupo
    )

    if grupo_filtro:

        usuarios_query = usuarios_query.filter(
            Grupo.nombre == grupo_filtro
        )

    usuarios = usuarios_query.order_by(
        Grupo.nombre,
        Usuario.nombre
    ).all()

    datos = []

    resumen = {}

    # ============================
    # RECORRER USUARIOS
    # ============================

    for usuario in usuarios:

        predicciones = PartidoEliminacion.query.filter(
            PartidoEliminacion.usuario_id == usuario.id,
            PartidoEliminacion.numero_partido.between(
                inicio,
                fin
            )
        ).order_by(
            PartidoEliminacion.numero_partido
        ).all()

        detalle = []

        total_puntos = 0

        equipos_acertados = 0    
        
        for pred in predicciones:

            partido_real = partidos_dict.get(
                pred.numero_partido
            )

            puntos_partido = 0

            acierto_local = False
            acierto_visitante = False
            acierto_campeon = False

            if acierto_local:
                equipos_acertados += 1

            if acierto_visitante:
                equipos_acertados += 1  

            if partido_real:

                # =====================================
                # VALIDACIÓN DEL CAMPEÓN
                # =====================================
                if fase == "Campeon":

                    acierto_campeon = (
                        partido_real
                        and pred.ganador
                        and partido_real.ganador
                        and pred.ganador == partido_real.ganador
                    )

                    puntos_partido = 20 if acierto_campeon else 0

                    total_puntos += puntos_partido

                    ganador_real = partido_real.ganador if partido_real else ""

                    detalle.append({
                       
                        "pred_ganador": pred.ganador,
                        "real_ganador": partido_real.ganador if partido_real else "",
                        "acierto_campeon": acierto_campeon,
                        "puntos": puntos_partido

                    })

                    continue


                if (fase == "Final"
                    and
                        pred.ganador
                        and
                        partido_real.ganador
                        and
                        pred.ganador == partido_real.ganador
                ):

                    acierto_campeon = True
                    puntos_partido += 20

                # ==========================
                # RESTO DE FASES
                # ==========================


                equipos_partido = {
                        partido_real.equipo_local,
                        partido_real.equipo_visitante
                }

                if pred.equipo_local in equipos_partido:

                        acierto_local = True
                        puntos_partido += puntos_fase
                        equipos_acertados += 1

                if pred.equipo_visitante in equipos_partido:

                        acierto_visitante = True
                        puntos_partido += puntos_fase
                        equipos_acertados += 1

            total_puntos += puntos_partido

            detalle.append({

                "numero": pred.numero_partido,

                "pred_local": pred.equipo_local,
                "pred_visitante": pred.equipo_visitante,

                "pred_ganador": pred.ganador,

                "real_local": partido_real.equipo_local if partido_real else "",
                "real_visitante": partido_real.equipo_visitante if partido_real else "",
                "real_ganador": partido_real.ganador if partido_real else "",

                "acierto_local": acierto_local,
                "acierto_visitante": acierto_visitante,
                "acierto_campeon": acierto_campeon,

                "aciertos": (
                    int(acierto_local)
                    + int(acierto_visitante)
                    + int(acierto_campeon)
                ),

                "puntos": puntos_partido

            })

        

        clave = str(total_puntos)

        if clave not in resumen:
            resumen[clave] = 0

        resumen[clave] += 1

        datos.append({

            "usuario": usuario,

            "grupo": usuario.grupo.nombre,

            "detalle": detalle,

            "total": total_puntos,

            "equipos_acertados": equipos_acertados


        })

    # ============================
    # ORDENAR
    # ============================

    datos = sorted(

        datos,

        key=lambda x: (

            x["grupo"],

            -x["total"],

            x["usuario"].nombre

        )

    )

    # ============================
    # AGRUPAR POR GRUPO
    # ============================

    grupos = defaultdict(list)

    for item in datos:

        grupos[item["grupo"]].append(item)

    # ============================
    # GRUPOS EXISTENTES
    # ============================

    lista_grupos = db.session.query(

        Grupo.nombre

    ).order_by(

        Grupo.nombre

    ).all()

    lista_grupos = [g.nombre for g in lista_grupos]

    return render_template(

        "usuario/validacion_clasificados.html",

        fase=fase,

        grupos=grupos,

        lista_grupos=lista_grupos,

        grupo_filtro=grupo_filtro,

        resumen=resumen,

        equipos_reales=sorted(equipos_reales),
        real_ganador=ganador_real if ganador_real else ""
        

    )