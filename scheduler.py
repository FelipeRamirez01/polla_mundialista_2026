from apscheduler.schedulers.background import BackgroundScheduler

from services.actualizacion_service import calcular_puntajes


scheduler = BackgroundScheduler()

scheduler.add_job(
    func=calcular_puntajes,
    trigger='interval',
    minutes=5
)

scheduler.start()