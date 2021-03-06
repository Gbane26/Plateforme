# Generated by Django 2.2.7 on 2019-11-25 12:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('specialisation', '0011_auto_20191125_1209'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('livecoding', '0011_auto_20191125_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=50)),
                ('niveau', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('specialite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialitecode', to='specialisation.Specialite')),
            ],
            options={
                'verbose_name': 'Code',
                'verbose_name_plural': 'Codes',
            },
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('titre_slug', models.SlugField(editable=False, max_length=255, null=True)),
                ('description', tinymce.models.HTMLField(verbose_name='description')),
                ('code_depart', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livecoding', to='livecoding.Code')),
            ],
            options={
                'verbose_name': 'Exercice',
                'verbose_name_plural': 'Exercices',
                'ordering': ('date_add',),
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
                'ordering': ('date_add',),
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
                'ordering': ('date_add',),
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
                'ordering': ('date_add',),
            },
        ),
    ]
