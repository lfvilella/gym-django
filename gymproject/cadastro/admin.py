from django.contrib import admin
from .models import Aluno, Funcionario, Pagamento, Plano, Planilha, ItemDaPlanilha, Periodizacao
from django.utils.html import format_html

class PagamentoInline(admin.StackedInline):
    model =  Pagamento
    max_num = 1

class AlunoAdmin(admin.ModelAdmin):
    fields =(
        ('aluno', 'plano'), 
        ('rg', 'cpf'),
        ('cidade', 'cep'),
        ('endereco', 'bairro', 'numero', 'complemento'), 
        ('telefone'),
        ('e_mail'),
        ('matriculado'),
    )
    list_display = ['aluno', 'plano', 'telefone']
    list_filter = ['plano', 'matriculado']
    search_fields = ['rg', 'aluno']
    inlines = [PagamentoInline]

admin.site.register(Aluno, AlunoAdmin)

class PagamentoAdmin(admin.ModelAdmin):
    list_display = ['data', 'aluno', 'phone_number', 'valor', 'pagamento_recebido']
    list_filter = ['pagamento_recebido', 'data']
    search_fields = ['aluno__aluno']
    date_hierarchy = 'data'

    def phone_number(self, obj):
        return format_html(f'<a href="https://api.whatsapp.com/send?phone={obj.aluno.telefone}">WhatsApp</a>')
    # phone_number.admin_order_field = 'aluno__telefone'

admin.site.register(Pagamento, PagamentoAdmin)

class FuncionarioAdmin(admin.ModelAdmin):
    fields =(
        ('nome_do_funcionario'), 
        ('rg', 'cpf'),
        ('cidade', 'cep'),
        ('endereco', 'bairro', 'numero', 'complemento'), 
        ('telefone'),
        ('e_mail'),
    )
    list_display = ['nome_do_funcionario']
    search_fields = ['rg', 'nome_do_funcionario']

admin.site.register(Funcionario, FuncionarioAdmin)

class PlanoAdmin(admin.ModelAdmin):
    list_display = ['modalidade', 'valor']

admin.site.register(Plano, PlanoAdmin)

class ItemDaPlanilhaInline(admin.StackedInline):
    model =  ItemDaPlanilha

class PeriodizacaoInline(admin.StackedInline):
    model =  Periodizacao

class PlanilhaAdmin(admin.ModelAdmin):
    list_display = ['aluno', 'data']
    search_fields = ['aluno']
    date_hierarchy = 'data'
    inlines = [ItemDaPlanilhaInline, PeriodizacaoInline]

admin.site.register(Planilha, PlanilhaAdmin)