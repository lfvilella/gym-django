from celery.schedules import crontab


CELERY_BEAT_SCHEDULE = {
    'gerar-pagamentos': {
        'task': 'cadastro.tasks.gerar_pagamentos',
        'schedule': crontab(minute=0, hour=0),
    },
    'gerar-pagamentos-passados': {
        'task': 'cadastro.tasks.gerar_pagamentos_passados',
        'schedule': crontab(day_of_month=[1], hour=1, minute=2),
    },
}
