# Generated by Django 2.1.3 on 2018-11-23 00:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0005_auto_20181122_1847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='area',
            old_name='area_Restringida',
            new_name='area_restringida',
        ),
        migrations.RenameField(
            model_name='area',
            old_name='areaSuperior',
            new_name='area_superior',
        ),
    ]
