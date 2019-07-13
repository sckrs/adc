# Generated by Django 2.1.3 on 2018-11-29 06:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0017_documento_periodo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AtaqueMasivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Documento', models.FileField(max_length=600, null=True, upload_to='MasiveAttack', verbose_name='Documento(s)')),
                ('periodo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='archivoDigital.PeriodoGestion', verbose_name='Periodo_Gestión')),
            ],
        ),
    ]
