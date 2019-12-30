# Generated by Django 2.2.7 on 2019-11-25 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialisation', '0013_auto_20191125_1538'),
        ('livecoding', '0012_code_exercice_resultatcompo_resultatexercice_testvalidation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultatcompo',
            name='niveau',
        ),
        migrations.AddField(
            model_name='resultatcompo',
            name='epreuve',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='epreuve', to='specialisation.Epreuve'),
        ),
        migrations.AlterField(
            model_name='resultatcompo',
            name='resultat_exercice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resultexoresultcompo', to='livecoding.Code', verbose_name='livecoding'),
        ),
        migrations.CreateModel(
            name='Langage_id',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lang_id', models.PositiveIntegerField()),
                ('status', models.BooleanField(default=True)),
                ('date_add', models.DateTimeField(auto_now_add=True)),
                ('date_upd', models.DateTimeField(auto_now=True)),
                ('specialite', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='specialitelangage', to='specialisation.Specialite')),
            ],
            options={
                'verbose_name': 'Langage_id',
                'verbose_name_plural': 'Langage_id',
                'ordering': ('date_add',),
            },
        ),
    ]
