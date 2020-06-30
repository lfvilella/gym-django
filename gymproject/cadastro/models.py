from django.db import models
from datetime import time, date
from users.models import CustomUser

class EnderecoMixin(models.Model):
    class Meta:
        abstract = True

    endereco = models.CharField(max_length=255, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    complemento = models.CharField(max_length=20, null=True, blank=True)
    cidade = models.CharField(max_length=50, null=True, blank=True, default='Fartura')
    cep = models.CharField(max_length=12, null=True, blank=True, default='18870-000')

    
class BaseModel(models.Model):
    class Meta:
        abstract = True

    cadastrado_em = models.DateTimeField(auto_now_add=True)
    ultima_alteracao = models.DateTimeField(auto_now=True)

class Funcionario(BaseModel, EnderecoMixin):
    nome_do_funcionario = models.CharField(max_length=255, null=False, blank=False)
    rg = models.CharField(max_length=15, null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=False, blank=False)
    e_mail = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f'{self.pk}: {self.nome_do_funcionario}'

class Aluno(BaseModel, EnderecoMixin):
    aluno = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    # nome_do_aluno = models.CharField(max_length=255, null=False, blank=False)
    rg = models.CharField(max_length=15, null=True, blank=True)
    cpf = models.CharField(max_length=15, null=True, blank=True)
    telefone = models.CharField(
        max_length=13, null=False, blank=False,
        default='55149',
        help_text=(
            'Preencha como o exemplo: 55149XXXXXXXX'
        )
    )
    e_mail = models.CharField(max_length=255, null=False, blank=False)
    plano = models.ForeignKey('Plano', on_delete=models.CASCADE)
    matriculado = models.BooleanField(
        default=True,
        help_text=(
            'Este campo será usado para gerar as cobranças mensais. '
            'Se o aluno estiver matriculado todo mês vamos gerar '
            'uma mensalidade.'
        )
    )
    
    def __str__(self):
        return f'{self.pk}: {self.aluno}'

    def gerar_pagamento_mensal(self, reference_date=None):
        reference_date = reference_date or date.today()
        pagamentos_no_mes = self.pagamento_set.filter(
            data__year=reference_date.year,
            data__month=reference_date.month,
        )
        if pagamentos_no_mes.exists():
            return

        data_matriculado = self.cadastrado_em
        valor_do_plano = self.plano.valor

        self.adicionar_pagamento(valor_do_plano, data_matriculado)

    def adicionar_pagamento(self, valor, reference_date=None):
        reference_date = reference_date or date.today()
        Pagamento.objects.create(
            aluno=self,
            data=reference_date,
            valor=valor,
            pagamento_recebido=False,
        )

class Pagamento(BaseModel):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data = models.DateField(max_length=20)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacao = models.TextField(null=True, blank=True)
    pagamento_recebido = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.aluno} - {self.data}'

class Plano(BaseModel):
    MODALIDADE_CHOICES = [
        ('musculacao', 'Musculação'),
        ('strongman', 'StrongMan'),
        ('powerlift', 'Powerlift'),
        ('crossfit', 'Crossfit'),
        ('feminino:circuito', 'Circuito [F]'),
        ('masculino:circuito', 'Circuito [M]'),
    ]
    modalidade = models.CharField(
        max_length=30, choices =MODALIDADE_CHOICES, null=True, blank=True
    )
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.modalidade} - {self.valor}'


WEEK_CHOICES = (
    ('Seg', 'Seg'),
    ('Ter', 'Ter'),
    ('Qua', 'Qua'),
    ('Qui', 'Qui'),
    ('Sex', 'Sex'),
    ('Sab', 'Sab'),
)
WORKOUT_CHOICES = (
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
    ('E', 'E'),
    ('F', 'F'),
)
class Periodizacao(models.Model):
    tabela = models.ForeignKey('Planilha', on_delete=models.CASCADE, null=True, blank=True)
    dia = models.CharField(
        max_length=30, choices=WEEK_CHOICES, null=True, blank=False
    )
    musculacao = models.CharField(
        max_length=30, choices=WORKOUT_CHOICES, null=True, blank=False
    )
    aerobico = models.IntegerField(null=True, blank=True)

class ItemDaPlanilha(models.Model):
    tabela = models.ForeignKey('Planilha', on_delete=models.CASCADE, null=True, blank=True)
    tipo_do_treino = models.CharField(
        max_length=30, choices=WORKOUT_CHOICES, null=True, blank=False
    )
    musculatura_do_treino = models.CharField(max_length=255, null=True, blank=False)
    exercicio = models.CharField(max_length=255, null=True, blank=False)
    series = models.IntegerField(null=True, blank=False)
    repeticao = models.IntegerField(null=True, blank=False)
    tecnica = models.CharField(max_length=255, null=True, blank=True)

class Planilha(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, null=True, blank=True)
    data = models.DateField(max_length=20, null=True, blank=False)

