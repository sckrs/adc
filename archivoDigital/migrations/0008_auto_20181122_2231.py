# Generated by Django 2.1.3 on 2018-11-23 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0007_auto_20181122_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arearestringida',
            name='area',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='AreaRestringida', to='archivoDigital.Area'),
        ),
    ]
