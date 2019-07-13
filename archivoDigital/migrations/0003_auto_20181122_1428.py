# Generated by Django 2.1.3 on 2018-11-22 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archivoDigital', '0002_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tipo', models.CharField(blank=True, choices=[('Dirección', 'Dirección'), ('Subdirección', 'Subdirección'), ('Coordinación/Jefatura', 'Coordinación/Jefatura')], default='Coordinación/Jefatura', max_length=25, null=True)),
                ('Nombre', models.CharField(choices=[(1, 'Dirección General'), (2, 'Dirección Academica'), (3, 'Subdirección de Investigación'), (4, 'Coordinación de Intercambios'), (5, 'Coordinación de Proyectos'), (6, 'Subdirección de Docencia'), (7, 'Coordinación de Servicios Escolares'), (8, 'Posgrado en la CDMX'), (9, 'Posgrado en LINGÜÍSTICA'), (10, 'Posgrado en OCCIDENTE'), (11, 'Posgrado en SURESTE'), (12, 'Posgrado en PACIFICO SUR'), (13, 'Posgrado en GOLFO'), (14, 'Posgrado en PENINSULAR'), (15, 'Posgrado en NORESTE'), (16, 'Subdirección de Bibliotecas'), (17, 'Subdirección de Difusión y Publicaciones'), (18, 'Coordinación de Publicaciones'), (19, 'Coordinación de difusión'), (20, 'Subdirección de Informática'), (21, 'Coordinación de Sistemas'), (22, 'Dirección de Vinculación'), (23, 'Dirección de Administración'), (24, 'Coordinación de Planeación y Control'), (25, 'Unidad de Trasparencia'), (26, 'Subdirección de Recursos Financieros'), (27, 'Jefatura de Presupuestos'), (28, 'Jefatura de Contabilidad'), (29, 'Jefatura de Recursos Humanos'), (30, 'Jefatura de Servicios Generales'), (31, 'Jefatura de Recursos Materiales'), (32, 'Coordinación de Archivo'), (33, 'Coordinación de Admin Financiera de Proyectos'), (34, 'Unidades Regionales'), (35, 'Dirección Regional Golfo'), (36, 'Jefatura de Administración Regional Golfo'), (37, 'Jefatura de Biblioteca Regional Golfo'), (38, 'Dirección Regional Pacifico Sur'), (39, 'Jefatura de Administración Pacifico Sur'), (40, 'Jefatura de Biblioteca Pacifico Sur'), (41, 'Dirección General Sureste'), (42, 'Jefatura de Administración Sureste'), (43, 'Jefatura de Biblioteca Sureste'), (44, 'Dirección General Occidente'), (45, 'Jefatura de Administración Occidente'), (46, 'Jefatura de Biblioteca Occidente'), (47, 'Dirección Regional Peninsular'), (48, 'Jefatura de Administración Peninsular'), (49, 'Jefatura de Biblioteca Peninsular'), (50, 'Dirección Regional Noreste'), (51, 'Jefatura de Administración Noreste'), (52, 'Jefatura de Biblioteca Noreste')], max_length=150)),
                ('Clave', models.CharField(blank=True, max_length=25, null=True)),
                ('Area_Restringida', models.BooleanField(default=False)),
                ('Prioridad', models.IntegerField(blank=True, choices=[(4, 4), (3, 3), (2, 2), (1, 1)], default=1, null=True)),
                ('password', models.CharField(blank=True, max_length=100, null=True)),
                ('areaSuperior', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='AreaSuperior', to='archivoDigital.Area')),
            ],
        ),
        migrations.AlterField(
            model_name='documento',
            name='Nombre',
            field=models.CharField(max_length=200, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='user',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='archivoDigital.Area', verbose_name='Área'),
        ),
    ]