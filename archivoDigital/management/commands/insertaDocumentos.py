import os
from django.core.management.base import BaseCommand, CommandError
from archivoDigital.models import Documento,Area,AsuntoArea,PeriodoGestion
from django.core.files import File
from unidecode import unidecode

AREAS = [
'Dirección General',
  'Dirección Académica',
    'Subdirección de Investigación',
      'Coordinación de Intercambios',
      'Coordinación de Proyectos',
    'Subdirección de Docencia',
      'Coordinación de Servicios Escolares',
      'Posgrado en la CDMX',
      'Posgrado en LINGÜÍSTICA',
      'Posgrado en OCCIDENTE',
      'Posgrado en SURESTE',
      'Posgrado en PACÍFICO SUR',
      'Posgrado en GOLFO',
      'Posgrado en PENINSULAR',
      'Posgrado en NORESTE',
    'Subdirección de Bibliotecas',
    'Subdirección de Difusión y Publicaciones',
      'Coordinación de Publicaciones',
      'Coordinación de difusión',
    'Subdirección de Informática',
      'Coordinación de Sistemas',
  'Dirección de Vinculación',
  'Dirección de Administración',
    'Coordinación de Planeación y Control',
    'Unidad de Transparencia',
    'Subdirección de Recursos Financieros',
      'Jefatura de Presupuestos',
      'Jefatura de Contabilidad',
      'Jefatura de Recursos Humanos',
      'Jefatura de Servicios Generales',
      'Jefatura de Recursos Materiales',
      'Coordinación de Archivo',
      'Coordinación de Administración Financiera de Proyectos',
'Unidades Regionales',
  'Dirección Regional Golfo',
    'Jefatura de Administración Regional Golfo',
    'Jefatura de Biblioteca Regional Golfo',
  'Dirección Regional Pacífico Sur',
    'Jefatura de Administración Pacífico Sur',
    'Jefatura de Biblioteca Pacífico Sur',
  'Dirección Regional Sureste',
    'Jefatura de Administración Sureste',
    'Jefatura de Biblioteca Sureste',
  'Dirección Regional Occidente',
    'Jefatura de Administración Occidente',
    'Jefatura de Biblioteca Occidente',
  'Dirección Regional Peninsular',
    'Jefatura de Administración Peninsular',
    'Jefatura de Biblioteca Peninsular',
  'Dirección Regional Noreste',
    'Jefatura de Administración Noreste',
    'Jefatura de Biblioteca Noreste',
]

AREAS_CAP = []
for i in AREAS:
    AREAS_CAP.append(i.upper())

class Command(BaseCommand):
    help = 'Entra a la url /home/sckrs/proyecto/media/CargaMasiva, extrae la carpeta .zip y recorre el dierctorio para insertar los documentos en el archivo digital'

    def handle(self, *args, **options):
        #borraDocs()
        getAsuntos('/media/sckrs/D/ARCHIVO DIGITAL 2015/CargaMasiva/DIRECCIÓN GENERAL','2015')
        #pruebaCargaDocs('/home/sckrs/proyecto/media/CargaMasiva/origen')
        self.stdout.write(self.style.SUCCESS('Successfully make something'))

def getAsuntos(dirName,periodo):
    parts=dirName.split('/')
    listOfFile = os.listdir(dirName)
    allFiles = list()
    asuntos = list()
    subareas = list()
    documentos = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            if entry in AREAS_CAP:
                subareas.append(entry)
            else:
                asuntos.append(entry)
        else:
            documentos.append(entry)

    area = Area.objects.get(nombre=AREAS[AREAS_CAP.index(parts[len(parts)-1])])
    periodoI = PeriodoGestion.objects.get(periodo=periodo)
    if len(documentos)>0:
        for documento in documentos:
            registraDoc(periodoI,area,'',documento,dirName)
    if len(asuntos)>0:
        for asunto in asuntos:
            registrAsuntos(area,1,periodo,os.path.join(dirName,asunto),asunto,'')
    if len(subareas)>0:
        for subarea in subareas:
            getAsuntos(os.path.join(dirName, subarea),periodo)

def registraDoc(periodo,area,asunto,documento,dir):
    areaCheca=Area.objects.get(nombre=area)

    reopen = open(os.path.join(dir,documento), 'rb')
    filedjango = File(reopen)

    documentoI = Documento()
    documentoI.periodo=periodo
    documentoI.area=area

    nameOffile = filedjango.name.split('/')

    if areaCheca.area_restringida:
        if asunto != '':
            documentoI.asunto=asunto
            documentoI.documento_restringido=True
            documentoI.documento.save(os.path.join(obtenUrl(periodo,area,asunto),nameOffile[len(nameOffile)-1]),filedjango, save=True)
        else:
            documentoI.documento_restringido=True
            documentoI.documento.save(os.path.join(obtenUrl(periodo,area,None),nameOffile[len(nameOffile)-1]),filedjango, save=True)
    else:
        if asunto != '':
            documentoI.asunto=asunto
            documentoI.documento.save(os.path.join(obtenUrl(periodo,area,asunto),nameOffile[len(nameOffile)-1]),filedjango, save=True)
        else:
            documentoI.documento.save(os.path.join(obtenUrl(periodo,area,None),nameOffile[len(nameOffile)-1]),filedjango, save=True)


def registrAsuntos(area,nivel,periodo,asuntopath,nombreasunto,padre):
    asunto = AsuntoArea.objects.none()
    subdirectorios=list()
    periodoI = PeriodoGestion.objects.get(periodo=periodo)

    if nivel==1:
        asunto = AsuntoArea.objects.create(nombre=nombreasunto.upper(),nivel=nivel)
    else:
        asunto = AsuntoArea.objects.create(nombre=nombreasunto.upper(),nivel=nivel,asuntoPadre=padre)
    asunto.area.add(area)
    asunto.periodo.add(periodoI)

    listOfFile = os.listdir(asuntopath)
    for entry in listOfFile:
        fullPath = os.path.join(asuntopath, entry)
        if os.path.isdir(fullPath):
            subdirectorios.append(entry)
        else:
            registraDoc(periodoI,area,asunto,entry,asuntopath)

    if len(subdirectorios)>0:
        for subdirectorio in subdirectorios:
            #print('area {}/ nivel {}/ periodo {}/ path {}/subdirectorio {}/asuntopadre {}'.format(area,nivel+1,periodo,os.path.join(asuntopath,subdirectorio),subdirectorio,asunto))
            registrAsuntos(area,nivel+1,periodo,os.path.join(asuntopath,subdirectorio),subdirectorio,asunto)

def borraDocs():
    Documento.objects.all().delete()
    AsuntoArea.objects.all().delete()

def pruebaCargaDocs(dirName):
    periodoI = PeriodoGestion.objects.get(periodo='2015')
    areaI = Area.objects.get(nombre='Dirección General')
    listOfFile = os.listdir(dirName)
    for item in listOfFile:
        reopen = open(os.path.join(dirName,item), 'rb')
        filedjango = File(reopen)
        documento = Documento()
        documento.periodo=periodoI
        documento.area=areaI
        print(filedjango.name)
        documento.documento.save('name.algo',filedjango, save=True)

def obtenUrl(año,area,asunto):
    areaInfo=Area.objects.get(nombre=area)
    if asunto == None:
        return ('{}/{}'.format(año,retornaUrlAreas(areaInfo,areaInfo.clave)))
    else :
        #aqui debe ir la linea de codigo que quita los caracteres especiales
        return ('{}/{}/{}'.format(año,retornaUrlAreas(areaInfo,areaInfo.clave),retornaUrlAsuntos(asunto,asunto.nivel)))

def retornaUrlAreas(area,clave):
    if clave != 'DG':
        areaArriba=Area.objects.get(nombre=area.area_superior)
        return os.path.join(retornaUrlAreas(areaArriba,areaArriba.clave),clave)
    else:
        return area.clave

def retornaUrlAsuntos(asunto,nivel):
    if nivel != 1:
        asuntoArriba=AsuntoArea.objects.get(pk=asunto.asuntoPadre.pk)
        return os.path.join(retornaUrlAsuntos(asuntoArriba,asuntoArriba.nivel),asunto.nombre)
    else:
        return asunto.nombre
