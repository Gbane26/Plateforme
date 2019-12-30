# Generated by Django 2.2.7 on 2019-11-23 09:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('specialisation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', tinymce.models.HTMLField(verbose_name='description')),
                ('code_depart', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('epreuve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveauexercice', to='specialisation.Epreuve')),
                ('specialite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialiteexercice', to='specialisation.Specialite')),
            ],
            options={
                'verbose_name': 'Exercice',
                'verbose_name_plural': 'Exercices',
            },
        ),
        migrations.CreateModel(
            name='TestValidation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_test', models.TextField()),
                ('resultat', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercicetest', to='livecoding.Exercice')),
            ],
            options={
                'verbose_name': 'TestValidation',
                'verbose_name_plural': 'TestValidations',
            },
        ),
        migrations.CreateModel(
            name='ResultatExercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_tentative', models.PositiveIntegerField()),
                ('code', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exerciceresultat', to='livecoding.Exercice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userresultat', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ResultatExercice',
                'verbose_name_plural': 'ResultatExercices',
            },
        ),
        migrations.CreateModel(
            name='ResultatCompo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('niveau', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='niveauresultatcompo', to='specialisation.Epreuve')),
                ('resultat_exercice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultexoresultcompo', to='livecoding.ResultatExercice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultatcompouser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'ResultatCompo',
                'verbose_name_plural': 'ResultatCompos',
            },
        ),
    ]
