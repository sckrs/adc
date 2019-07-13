from django.core.management.base import BaseCommand, CommandError
from archivoDigital.models import Area
from unidecode import unidecode

AREAS=[{'tipo':'Dirección','nombre':'Dirección General','clave':'DG','area_superior':None,'area_restringida':False},
{'tipo':'Dirección','nombre':'	Dirección Académica','clave':'DAC','area_superior':'Dirección General','area_restringida':False},
{'tipo':'Subdirección','nombre':'Subdirección de Investigación','clave':1,'area_superior':'Dirección Académica','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Intercambios','clave':1.2,'area_superior':'Subdirección de Investigación','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Proyectos','clave':	1.3,'area_superior':'Subdirección de Investigación','area_restringida':True},
{'tipo':'Subdirección','nombre':'Subdirección de Bibliotecas','clave':2,'area_superior':'Dirección Académica','area_restringida':False},
{'tipo':'Subdirección','nombre':'	Subdirección de Difusión y Publicaciones','clave':3,'area_superior':'Dirección Académica','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de difusión','clave':3.1,'area_superior':'Subdirección de Difusión y Publicaciones','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'	Coordinación de Publicaciones','clave':3.2,'area_superior':'Subdirección de Difusión y Publicaciones','area_restringida':True},
{'tipo':'Subdirección','nombre':'Subdirección de Docencia','clave':4,'area_superior':'Dirección Académica','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Servicios Escolares','clave':4.1,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en la CDMX','clave':	4.2,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en LINGÜISTICA','clave':4.3,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en OCCIDENTE','clave':4.4,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en SURESTE','clave':4.5,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en PACÍFICO SUR','clave':4.6,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en GOLFO','clave':4.7,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en PENINSULAR','clave':4.8,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Posgrado en NORESTE','clave':4.9,'area_superior':'Subdirección de Docencia','area_restringida':False},
{'tipo':'Subdirección','nombre':'Subdirección de Informática','clave':5,'area_superior':'Dirección Académica','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Sistemas','clave':5.1,'area_superior':'Subdirección de Informática','area_restringida':False},
{'tipo':'Dirección','nombre':'Dirección de Vinculación','clave':'DV','area_superior':'Dirección General','area_restringida':True},
{'tipo':'Dirección','nombre':'	Dirección de Administración','clave':'DA','area_superior':'Dirección General','area_restringida':False},
{'tipo':'Subdirección','nombre':'Unidad de Transparencia','clave':'UT','area_superior':'Dirección de Administración','area_restringida':False},
{'tipo':'Subdirección','nombre':'Coordinación de Planeación y Control','clave':'CPC','area_superior':'Dirección de Administración','area_restringida':False},
{'tipo':'Subdirección','nombre':'Subdirección de Recursos Financieros','clave':1,'area_superior':'Dirección de Administración','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Contabilidad','clave':1.1,'area_superior':'Subdirección de Recursos Financieros','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Presupuestos','clave':1.2,'area_superior':'Subdirección de Recursos Financieros','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Archivo','clave':1.3,'area_superior':'Subdirección de Recursos Financieros','area_restringida':True},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Recursos Humanos','clave':1.4,'area_superior':'Subdirección de Recursos Financieros','area_restringida':True},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Recursos Materiales','clave':1.5,'area_superior':'Subdirección de Recursos Financieros','area_restringida':True},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Servicios Generales','clave':1.6,'area_superior':'Subdirección de Recursos Financieros','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Coordinación de Administración Financiera de Proyectos','clave':1.7,'area_superior':'Subdirección de Recursos Financieros','area_restringida':True},
{'tipo':'Dirección','nombre':'Unidades Regionales','clave':'UR','area_superior':'Dirección General','area_restringida':False},
{'tipo':'Subdirección','nombre':'Dirección Regional Golfo','clave':'DRGF.1','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Regional Golfo','clave':1.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Regional Golfo','clave':1.2,'area_superior':'Dirección Regional Golfo','area_restringida':True},
{'tipo':'Subdirección','nombre':'Dirección Regional Pacífico Sur','clave':'DRPS.2','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Pacífico Sur','clave':2.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Pacífico Sur','clave':2.2,'area_superior':'Dirección Regional Golfo','area_restringida':True},
{'tipo':'Subdirección','nombre':'Dirección Regional Sureste','clave':'DGSR.3','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Sureste','clave':3.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Sureste','clave':3.2,'area_superior':'Dirección Regional Golfo','area_restringida':True},
{'tipo':'Subdirección','nombre':'Dirección Regional Occidente','clave':'DROC.4','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Occidente','clave':4.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Occidente','clave':4.2,'area_superior':'Dirección Regional Golfo','area_restringida':True},
{'tipo':'Subdirección','nombre':'Dirección Regional Peninsular','clave':'DRPR.5','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Peninsular','clave':5.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Peninsular','clave':5.2,'area_superior':'Dirección Regional Golfo','area_restringida':True},
{'tipo':'Subdirección','nombre':'Dirección Regional Noreste','clave':'DRNE.6','area_superior':'Unidades Regionales','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Administración Noreste','clave':6.1,'area_superior':'Dirección Regional Golfo','area_restringida':False},
{'tipo':'Coordinación/Jefatura','nombre':'Jefatura de Biblioteca Noreste','clave':6.2,'area_superior':'Dirección Regional Golfo','area_restringida':True}]

class Command(BaseCommand):
    help = 'Este comando poblara la tabla de áreas'

    def handle(self, *args, **kwargs):
        for i in AREAS:
            area = Area.objects.create(tipo=i['tipo'],nombre=i['nombre'],clave=i['clave'],area_restringida=i['area_restringida'])
            if i['clave']=='DG':
                area.prioridad=4
            elif i['clave']!='DG' and i['tipo']=='Dirección':
                area.prioridad=3
            elif i['tipo']=='Subdirección':
                area.prioridad=2

            if i['clave']!='DG':
                area.area_superior=getPadre(i['area_superior'])

            area.save()
        self.stdout.write(self.style.SUCCESS('Se ha poblado la tabla de areas del ADC'))

def getPadre(nombre):
    return Area.objects.get(nombre=nombre)
