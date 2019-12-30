# Generated by Django 2.2.7 on 2019-11-23 17:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('livecoding', '0005_auto_20191123_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='date_add',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='code',
            name='date_upd',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='code',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
