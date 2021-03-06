# Generated by Django 2.2.3 on 2019-08-21 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0012_periodizacao_tabela'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdaplanilha',
            name='exercicio',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemdaplanilha',
            name='repeticao',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='itemdaplanilha',
            name='series',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='itemdaplanilha',
            name='tecnica',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='itemdaplanilha',
            name='tipo_do_treino',
            field=models.CharField(choices=[('treino_A', 'A'), ('treino_B', 'B'), ('treino_C', 'C'), ('treino_D', 'D'), ('treino_E', 'E'), ('treino_F', 'F')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='periodizacao',
            name='aerobico',
            field=models.IntegerField(null=True),
        ),
    ]
