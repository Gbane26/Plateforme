# Generated by Django 2.2.7 on 2019-11-27 00:05

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('livecoding', '0015_auto_20191126_2259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='code',
            name='consige',
            field=tinymce.models.HTMLField(null=True, verbose_name='consigne a respecter '),
        ),
    ]
