import logging

from datetime import date, datetime, timedelta
from gymproject import celery_app
from .models import Aluno
from .models import Pagamento
from .models import Plano


@celery_app.task
def gerar_pagamentos(reference_date=None):
    reference_date = reference_date or date.today()
    alunos_matriculados = Aluno.objects.filter(matriculado=True)
    for aluno in alunos_matriculados:
        if aluno.cadastrado_em.date() == reference_date:
            logging.info('Gerando pagamento aluno: %s', aluno)
            aluno.gerar_pagamento_mensal(reference_date)

@celery_app.task
def gerar_pagamentos_passados(reference_date=None):
    reference_date = reference_date or date.today()
    last_month = reference_date - datetime.timedelta(days=1)
    alunos_matriculados = Aluno.objects.filter(matriculado=True)
    for aluno in alunos_matriculados:
        logging.info('Gerando pagamento aluno: %s', aluno)
        aluno.gerar_pagamento_mensal(last_month)