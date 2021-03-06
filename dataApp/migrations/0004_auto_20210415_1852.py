# Generated by Django 2.2 on 2021-04-15 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataApp', '0003_auto_20210411_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='therapist_who_treats',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='dataApp.Therapist'),
        ),
    ]
