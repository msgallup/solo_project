# Generated by Django 2.2 on 2021-04-11 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataApp', '0002_auto_20210409_0018'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='evaluations',
            new_name='evaluation',
        ),
        migrations.RenameField(
            model_name='client',
            old_name='no_shows',
            new_name='no_show',
        ),
    ]
