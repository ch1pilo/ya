# Generated by Django 5.1.2 on 2024-11-14 02:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp1', '0002_tipouser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postuladodacademicos',
            name='idPostulado',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='academicos', to='myApp1.postulado'),
        ),
    ]
