# Generated by Django 2.2.7 on 2019-11-26 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('specialisation', '0016_resultatepreuve_user_moyenne'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resultatepreuve',
            name='user_moyenne',
        ),
    ]
