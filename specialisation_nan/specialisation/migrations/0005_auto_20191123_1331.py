# Generated by Django 2.2.7 on 2019-11-23 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('specialisation', '0004_auto_20191123_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userspecialite',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_specialite', to=settings.AUTH_USER_MODEL),
        ),
    ]
