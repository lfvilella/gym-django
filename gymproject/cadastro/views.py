from django.shortcuts import render
from .models import Planilha, ItemDaPlanilha, Periodizacao
import collections

def treino(request):
    # User:
    username = None
    if request.user.is_authenticated:
        username = request.user.username

    # Date:
    data_planilha = Planilha.objects.filter(aluno__pk=1).order_by('-data').first().data

    # Agrupando Treino:
    ultima_planilha = Planilha.objects.filter(aluno__aluno=request.user).order_by('-data').first()
    items_da_planilha = ItemDaPlanilha.objects.filter(tabela=ultima_planilha) 
    agrupador = collections.defaultdict(list)
    for item in items_da_planilha:
        agrupador[item.tipo_do_treino].append({
                'musculatura': item.musculatura_do_treino,
                'exercicio': item.exercicio,
                'series': item.series,
                'repeticao': item.repeticao,
                'tecnica': item.tecnica
            })

    # Agrupando Periodizacao:
    items_da_periodizacao = Periodizacao.objects.filter(tabela=ultima_planilha)
    agrupador_periodizacao = collections.defaultdict(list)
    for item in items_da_periodizacao:
        agrupador_periodizacao[item.dia].append({
            'musculacao': item.musculacao,
            'aerobico': item.aerobico
        })

    context = {
        'username': username,
        'data_planilha': data_planilha,
        'items_da_planilha': items_da_planilha,
        'agrupador': list(agrupador.items()), # Para sair certo no template
        'agrupador_periodizacao': list(agrupador_periodizacao.items()) # Para sair certo no template
    }
    return render(request, 'planilha.html', context)