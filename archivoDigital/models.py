# -*- coding: utf-8 -*-
import zipfile
import datetime
from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth import models as auth_models
from private_files import PrivateFileField
from django.contrib.auth.hashers import make_password
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from archivoDigital.send_email import senderMany


AREA_CHOICES = (
    ('Dirección General','Dirección General'),
      ('Dirección Académica','Dirección Académica'),
        ('Subdirección de Investigación','Subdirección de Investigación'),
          ('Coordinación de Intercambios','Coordinación de Intercambios'),
          ('Coordinación de Proyectos','Coordinación de Proyectos'),
        ('Subdirección de Docencia','Subdirección de Docencia'),
          ('Coordinación de Servicios Escolares','Coordinación de Servicios Escolares'),
          ('Posgrado en la CDMX','Posgrado en la CDMX'),
          ('Posgrado en LINGÜISTICA','Posgrado en LINGÜISTICA'),
          ('Posgrado en OCCIDENTE','Posgrado en OCCIDENTE'),
          ('Posgrado en SURESTE','Posgrado en SURESTE'),
          ('Posgrado en PACÍFICO SUR','Posgrado en PACÍFICO SUR'),
          ('Posgrado en GOLFO','Posgrado en GOLFO'),
          ('Posgrado en PENINSULAR','Posgrado en PENINSULAR'),
          ('Posgrado en NORESTE','Posgrado en NORESTE'),
        ('Subdirección de Bibliotecas','Subdirección de Bibliotecas'),
        ('Subdirección de Difusión y Publicaciones','Subdirección de Difusión y Publicaciones'),
          ('Coordinación de Publicaciones','Coordinación de Publicaciones'),
          ('Coordinación de difusión','Coordinación de difusión'),
        ('Subdirección de Informática','Subdirección de Informática'),
          ('Coordinación de Sistemas','Coordinación de Sistemas'),
      ('Dirección de Vinculación','Dirección de Vinculación'),
      ('Dirección de Administración','Dirección de Administración'),
        ('Coordinación de Planeación y Control','Coordinación de Planeación y Control'),
        ('Unidad de Transparencia','Unidad de Transparencia'),
        ('Subdirección de Recursos Financieros','Subdirección de Recursos Financieros'),
          ('Jefatura de Presupuestos','Jefatura de Presupuestos'),
          ('Jefatura de Contabilidad','Jefatura de Contabilidad'),
          ('Jefatura de Recursos Humanos','Jefatura de Recursos Humanos'),
          ('Jefatura de Servicios Generales','Jefatura de Servicios Generales'),
          ('Jefatura de Recursos Materiales','Jefatura de Recursos Materiales'),
          ('Coordinación de Archivo','Coordinación de Archivo'),
          ('Coordinación de Administración Financiera de Proyectos','Coordinación de Administración Financiera de Proyectos'),
    ('Unidades Regionales','Unidades Regionales'),
      ('Dirección Regional Golfo','Dirección Regional Golfo'),
        ('Jefatura de Administración Regional Golfo','Jefatura de Administración Regional Golfo'),
        ('Jefatura de Biblioteca Regional Golfo','Jefatura de Biblioteca Regional Golfo'),
      ('Dirección Regional Pacífico Sur','Dirección Regional Pacífico Sur'),
        ('Jefatura de Administración Pacífico Sur','Jefatura de Administración Pacífico Sur'),
        ('Jefatura de Biblioteca Pacífico Sur','Jefatura de Biblioteca Pacífico Sur'),
      ('Dirección Regional Sureste','Dirección Regional Sureste'),
        ('Jefatura de Administración Sureste','Jefatura de Administración Sureste'),
        ('Jefatura de Biblioteca Sureste','Jefatura de Biblioteca Sureste'),
      ('Dirección Regional Occidente','Dirección Regional Occidente'),
        ('Jefatura de Administración Occidente','Jefatura de Administración Occidente'),
        ('Jefatura de Biblioteca Occidente','Jefatura de Biblioteca Occidente'),
      ('Dirección Regional Peninsular','Dirección Regional Peninsular'),
        ('Jefatura de Administración Peninsular','Jefatura de Administración Peninsular'),
        ('Jefatura de Biblioteca Peninsular','Jefatura de Biblioteca Peninsular'),
      ('Dirección Regional Noreste','Dirección Regional Noreste'),
        ('Jefatura de Administración Noreste','Jefatura de Administración Noreste'),
        ('Jefatura de Biblioteca Noreste','Jefatura de Biblioteca Noreste'),)

TIPO_CHOICES = (('Dirección','Dirección'),
                ('Subdirección','Subdirección'),
                ('Coordinación/Jefatura','Coordinación/Jefatura'),)

PRIORIDAD_CHOICES = ((4,4),
                     (3,3),
                     (2,2),
                     (1,1),)

def defineRuta(nombre,file):
    return 'adc/{}'.format(file)

def is_owner(request, instance):
    if (not request.user.is_anonymous) and request.user.is_authenticated:
        if instance.documento_restringido:
            return check_can_access_to_area(request.user.area,instance.area) and instance.pk in request.session['docsUnRestricted']
        else:
            return check_can_access_to_area(request.user.area,instance.area)
    else:
        return False

def check_can_access_to_area(areausuario,areapretendeacceder):
    if areausuario.clave == 'DG':
        return True
    else:
        if areausuario == areapretendeacceder:
            return True
        else:
            if areausuario.prioridad < areapretendeacceder.prioridad:
                return False
            else:
                areaSuperiorDoc=retornaBreadCumbAreas(areapretendeacceder,[])
                return areausuario in areaSuperiorDoc

class Documento(models.Model):
    periodo = models.ForeignKey('PeriodoGestion',on_delete=models.CASCADE,blank=False,null=True,verbose_name=_('Periodo_Gestión'))
    area = models.ForeignKey('Area',on_delete=models.CASCADE,blank=False,verbose_name=_('Área pertenece(n)'))
    asunto = models.ForeignKey('AsuntoArea',on_delete=models.CASCADE,blank=True,null=True,verbose_name=_('Asunto_pertenece(n)'))
    nombre = models.CharField("Nombre", max_length = 1200)
    documento = PrivateFileField("file", upload_to=defineRuta,max_length=1200,blank=False,condition = is_owner)
    documento_restringido = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs ):
        self.nombre=self.documento.name
        super(Documento, self ).save(*args,**kwargs)

    def Nombre(self):
        parts=self.nombre.split('/')
        return parts[len(parts)-1]

class DocumentoRestringido(models.Model):
    periodo = models.ForeignKey('PeriodoGestion',default='2015',on_delete=models.CASCADE,blank=False,verbose_name=_('Año'))
    area = models.ForeignKey('Area',default=None,on_delete=models.CASCADE,null=True,blank=False,verbose_name=_('Área pertenece'))
    password = models.CharField(max_length=100,null=True,blank=False)

    def __str__(self):
        return '{}/{}'.format(self.periodo,self.area)

    def save(self, *args, **kwargs ):
        self.nps=self.password
        self.password=make_password(self.password)
        super(DocumentoRestringido, self ).save(*args,**kwargs)

def asegura_docs(sender, instance, created,**kwargs):
    if created:
        area=Area.objects.get(pk=instance.area.pk)
        Documento.objects.filter(periodo=instance.periodo,area=area).update(documento_restringido=True)
        areaS=retornaBreadCumbAreas(instance.area,[])
        listaContactos=[]
        for area in areaS:
            usuarioEmail=User.objects.filter(area=area)
            if usuarioEmail.exists():
                for usr in usuarioEmail:
                    listaContactos.append(usr.email)
        senderMany(listaContactos,'Claves de acceso a',instance.nps,'{}/{}'.format(instance.periodo,instance.area.nombre))

post_save.connect(asegura_docs,sender=DocumentoRestringido)

class Area(models.Model):
    tipo = models.CharField(max_length=25,choices=TIPO_CHOICES,default='Coordinación/Jefatura',blank=False)
    nombre = models.CharField(unique=True,max_length=60,choices=AREA_CHOICES,)
    clave = models.CharField(max_length=15,default='inserte clave',blank=False)
    area_superior = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True, related_name='AreaSuperior')
    prioridad = models.IntegerField(choices=PRIORIDAD_CHOICES,default=1,blank=False)
    area_restringida = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

    class Meta:
        ordering = ['pk']

class AreaRestringida(models.Model):
    area = models.OneToOneField('Area',on_delete=models.CASCADE,blank=False,null=False,related_name='AreaRestringida')
    password = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.area.nombre

    def save(self, *args, **kwargs ):
        self.nps=self.password
        self.password=make_password(self.password)
        print ('el password va a ser seteado {0}'.format(self.nps))
        super(AreaRestringida, self ).save(*args,**kwargs)
        print ('se guardo {0}'.format(self.nps))

def enviaNotificacion(sender, instance, created,**kwargs):
    if created:
        areaS=retornaBreadCumbAreas(instance.area,[])
        listaContactos=[]
        for area in areaS:
            usuarioEmail=User.objects.filter(area=area)
            if usuarioEmail.exists():
                for usr in usuarioEmail:
                    listaContactos.append(usr.email)
        senderMany(listaContactos,'Actualización de claves de acceso',instance.nps,instance.area.nombre)

post_save.connect(enviaNotificacion,sender=AreaRestringida)

class UserManager(auth_models.BaseUserManager):

    def create_user(self, email,first_name,last_name,password=None):
        if not email:
            raise ValueError('El usuario debe tener un e-mail')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.first_name=first_name
        user.last_name=last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name,password):
        user = self.create_user(email,first_name,last_name, password=password)
        user.is_superuser = user.is_staff = True
        user.first_name=first_name
        user.last_name=last_name
        user.save(using=self._db)
        return user

class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True,verbose_name=_('Correo Electrónico'))
    first_name = models.CharField(max_length=150,blank=False,verbose_name=_('Nombre(s)'))
    last_name = models.CharField(max_length=150,blank=False,verbose_name=_('Apellidos(s)'))
    is_staff = models.BooleanField(default=False,verbose_name=_('Administrador'))
    is_active = models.BooleanField(default=True,verbose_name=_('Activo'))
    date_joined = models.DateTimeField(auto_now_add=True,verbose_name=_('Fecha de alta'))
    changePass = models.CharField(max_length=30,verbose_name=_('Cambio de password'), null=True, blank=True)

    phone = models.CharField(max_length=150,null=True,blank=True,verbose_name=_('Teléfono'))
    extension = models.CharField(max_length=150,null=True,blank=True,verbose_name=_('Extensión'))
    area = models.ForeignKey('Area',on_delete=models.CASCADE,null=True,blank=False,verbose_name=_('Área'))
    cargo = models.CharField(max_length=150,default='Cargo del nuevo usuario',blank=False,verbose_name=_('Cargo'))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = _('Usuario')
        verbose_name_plural = _('Usuarios')
        ordering = ('id', )

    def __unicode__(self):
        return u'{0} ({1})'.format(self.get_full_name(), self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)

class PeriodoGestion(models.Model):
    YEAR_CHOICES = []
    for r in range(2015, (datetime.datetime.now().year+1)):
        YEAR_CHOICES.append((r,r))

    periodo = models.IntegerField(_('Año'),choices=YEAR_CHOICES, default=datetime.datetime.now().year,unique=True)

    def __str__(self):
        return '{0}'.format(self.periodo)

    class Meta:
        verbose_name = 'Periodo de Gestion'
        verbose_name_plural = 'Periodos de Gestion'

class AsuntoArea(models.Model):
    nombre = models.CharField(max_length=150,unique=False,verbose_name=_('Nombre'))
    area = models.ManyToManyField('Area',verbose_name=_('Área'))
    periodo = models.ManyToManyField('PeriodoGestion',blank=False, related_name='Periodo_Asunto',verbose_name=_('Periodo_asunto'))
    nivel = models.IntegerField(default=1,verbose_name=_('Nivel'))
    asuntoPadre = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True, related_name='AsuntoPadre',verbose_name=_('Asunto_superior'))

    def __str__(self):
        return self.nombre

    def area_del_asunto(self):
        return ",".join([str(p) for p in self.area.all()])

    class Meta:
        ordering = ['pk']

class ReporteInsidencias(models.Model):
    hora = models.DateTimeField('hora',null=True,blank=False)
    usuario = models.ForeignKey('User',on_delete=models.CASCADE,null=True,blank=False,verbose_name=_('Usuario'))
    causa = models.CharField(max_length=150,unique=False,verbose_name=_('Causa'))
##########################################

def retornaBreadCumbAreas(area,ar):
    if area.clave != 'DG':
        areaArriba=Area.objects.get(nombre=area.area_superior)
        ar.append(area)
        return retornaBreadCumbAreas(areaArriba,ar)
    else:
        ar.append(area)
        return ar
