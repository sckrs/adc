# Generated by Django 2.1.3 on 2018-12-01 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0024_auto_20181130_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentorestringido',
            name='area',
            field=models.ForeignKey(default=None,null=True, on_delete=django.db.models.deletion.CASCADE, to='archivoDigital.Area', verbose_name='Área pertenece'),
        ),
    ]