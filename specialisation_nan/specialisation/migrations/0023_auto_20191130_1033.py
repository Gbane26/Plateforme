# Generated by Django 2.2.7 on 2019-11-30 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialisation', '0022_remove_resultatepreuve_user_moyenne'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultatepreuve',
            name='code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resultat_livecoding', to='livecoding.Code'),
        ),
    ]
