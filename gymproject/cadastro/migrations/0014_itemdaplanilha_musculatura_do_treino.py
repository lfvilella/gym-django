# Generated by Django 2.2.3 on 2019-08-21 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastro', '0013_auto_20190821_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='itemdaplanilha',
            name='musculatura_do_treino',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
