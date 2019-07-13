# Generated by Django 2.1.3 on 2018-11-30 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0021_auto_20181130_1230'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsuntoArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('nivel', models.IntegerField(default=1, verbose_name='Nivel')),
                ('area', models.ManyToManyField(to='archivoDigital.Area', verbose_name='Área')),
                ('asuntoPadre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AsuntoPadre', to='archivoDigital.AsuntoArea', verbose_name='Asunto_superior')),
                ('periodo', models.ManyToManyField(related_name='Periodo_Asunto', to='archivoDigital.PeriodoGestion', verbose_name='Periodo_asunto')),
            ],
        ),
    ]