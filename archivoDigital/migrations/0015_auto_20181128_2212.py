# Generated by Django 2.1.3 on 2018-11-29 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0014_auto_20181128_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoGestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.IntegerField(choices=[(2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018)], default=2018, unique=True, verbose_name='Año')),
            ],
            options={
                'verbose_name': 'Periodo de Gestion',
                'verbose_name_plural': 'Periodos de Gestion',
            },
        ),
        migrations.AlterField(
            model_name='area',
            name='nombre',
            field=models.CharField(choices=[('Dirección General', 'Dirección General'), ('Dirección Académica', 'Dirección Académica'), ('Subdirección de Investigación', 'Subdirección de Investigación'), ('Coordinación de Intercambios', 'Coordinación de Intercambios'), ('Coordinación de Proyectos', 'Coordinación de Proyectos'), ('Subdirección de Docencia', 'Subdirección de Docencia'), ('Coordinación de Servicios Escolares', 'Coordinación de Servicios Escolares'), ('Posgrado en la CDMX', 'Posgrado en la CDMX'), ('Posgrado en LINGÜÍSTICA', 'Posgrado en LINGÜÍSTICA'), ('Posgrado en OCCIDENTE', 'Posgrado en OCCIDENTE'), ('Posgrado en SURESTE', 'Posgrado en SURESTE'), ('Posgrado en PACÍFICO SUR', 'Posgrado en PACÍFICO SUR'), ('Posgrado en GOLFO', 'Posgrado en GOLFO'), ('Posgrado en PENINSULAR', 'Posgrado en PENINSULAR'), ('Posgrado en NORESTE', 'Posgrado en NORESTE'), ('Subdirección de Bibliotecas', 'Subdirección de Bibliotecas'), ('Subdirección de Difusión y Publicaciones', 'Subdirección de Difusión y Publicaciones'), ('Coordinación de Publicaciones', 'Coordinación de Publicaciones'), ('Coordinación de difusión', 'Coordinación de difusión'), ('Subdirección de Informática', 'Subdirección de Informática'), ('Coordinación de Sistemas', 'Coordinación de Sistemas'), ('Dirección de Vinculación', 'Dirección de Vinculación'), ('Dirección de Administración', 'Dirección de Administración'), ('Coordinación de Planeación y Control', 'Coordinación de Planeación y Control'), ('Unidad de Transparencia', 'Unidad de Transparencia'), ('Subdirección de Recursos Financieros', 'Subdirección de Recursos Financieros'), ('Jefatura de Presupuestos', 'Jefatura de Presupuestos'), ('Jefatura de Contabilidad', 'Jefatura de Contabilidad'), ('Jefatura de Recursos Humanos', 'Jefatura de Recursos Humanos'), ('Jefatura de Servicios Generales', 'Jefatura de Servicios Generales'), ('Jefatura de Recursos Materiales', 'Jefatura de Recursos Materiales'), ('Coordinación de Archivo', 'Coordinación de Archivo'), ('Coordinación de Admin Financiera de Proyectos', 'Coordinación de Admin Financiera de Proyectos'), ('Unidades Regionales', 'Unidades Regionales'), ('Dirección Regional Golfo', 'Dirección Regional Golfo'), ('Jefatura de Administración Regional Golfo', 'Jefatura de Administración Regional Golfo'), ('Jefatura de Biblioteca Regional Golfo', 'Jefatura de Biblioteca Regional Golfo'), ('Dirección Regional Pacífico Sur', 'Dirección Regional Pacífico Sur'), ('Jefatura de Administración Pacífico Sur', 'Jefatura de Administración Pacífico Sur'), ('Jefatura de Biblioteca Pacífico Sur', 'Jefatura de Biblioteca Pacífico Sur'), ('Dirección General Sureste', 'Dirección General Sureste'), ('Jefatura de Administración Sureste', 'Jefatura de Administración Sureste'), ('Jefatura de Biblioteca Sureste', 'Jefatura de Biblioteca Sureste'), ('Dirección General Occidente', 'Dirección General Occidente'), ('Jefatura de Administración Occidente', 'Jefatura de Administración Occidente'), ('Jefatura de Biblioteca Occidente', 'Jefatura de Biblioteca Occidente'), ('Dirección Regional Peninsular', 'Dirección Regional Peninsular'), ('Jefatura de Administración Peninsular', 'Jefatura de Administración Peninsular'), ('Jefatura de Biblioteca Peninsular', 'Jefatura de Biblioteca Peninsular'), ('Dirección Regional Noreste', 'Dirección Regional Noreste'), ('Jefatura de Administración Noreste', 'Jefatura de Administración Noreste'), ('Jefatura de Biblioteca Noreste', 'Jefatura de Biblioteca Noreste')], max_length=150),
        ),
    ]