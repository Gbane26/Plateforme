# Generated by Django 2.2.7 on 2019-11-25 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('livecoding', '0012_code_exercice_resultatcompo_resultatexercice_testvalidation'),
        ('specialisation', '0011_auto_20191125_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='epreuve',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resultat_code', to='livecoding.Code'),
        ),
        migrations.AddField(
            model_name='resultatepreuve',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resultat_code', to='livecoding.ResultatExercice'),
        ),
    ]