# Generated by Django 2.2.7 on 2019-11-23 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('livecoding', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercice',
            options={'ordering': ('date_add',), 'verbose_name': 'Exercice', 'verbose_name_plural': 'Exercices'},
        ),
        migrations.AlterModelOptions(
            name='resultatcompo',
            options={'ordering': ('date_add',), 'verbose_name': 'ResultatCompo', 'verbose_name_plural': 'ResultatCompos'},
        ),
        migrations.AlterModelOptions(
            name='resultatexercice',
            options={'ordering': ('date_add',), 'verbose_name': 'ResultatExercice', 'verbose_name_plural': 'ResultatExercices'},
        ),
        migrations.AlterModelOptions(
            name='testvalidation',
            options={'ordering': ('date_add',), 'verbose_name': 'TestValidation', 'verbose_name_plural': 'TestValidations'},
        ),
    ]
