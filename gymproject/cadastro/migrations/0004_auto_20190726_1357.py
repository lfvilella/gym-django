# Generated by Django 2.2.3 on 2019-07-26 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0003_auto_20190726_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='modalidade',
            field=models.CharField(blank=True, choices=[('musculacao', 'Musculação'), ('strongman', 'StrongMan'), ('powerlift', 'Powerlift'), ('crossfit', 'Crossfit'), ('feminino:circuito', 'Circuito [F]'), ('masculino:circuito', 'Circuito [M]')], max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='Modalidade',
        ),
    ]
