# -*- coding: utf-8 -*-

import os
from django.conf import settings
from django.http import JsonResponse
from archivoDigital.decorators import area_user_is_restricted
from django.contrib.auth.hashers import make_password,check_password
from django.forms import ValidationError
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from archivoDigital.models import User,Documento,PeriodoGestion,Area,AsuntoArea,AreaRestringida,DocumentoRestringido,ReporteInsidencias
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views import View
from archivoDigital.forms import sender

class userLogin(View):
    def post(self,request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(email=email, password=password)
        if user:
            request.session['intentos']=0
            request.session['intentosDoc']=0
            request.session['unrestricted']=True
            request.session['areaRestringida']=False
            request.session['areasUnrestricted']=[]
            request.session['docsUnRestricted']=[]
            login(request,user)
            return redirect('/archivoDigital/')
        else:
            try:
                usuario = User.objects.get(email=request.POST.get('email'))
            except User.DoesNotExist:
                usuario = None

            if usuario != None:
                if not usuario.is_active:
                    mensaje = 'Su usuario ha sido bloqueado, contacte al administrador para desbloquear su cuenta.'
                else:
                    mensaje = "Contraseña incorrecta."
            else:
                mensaje = "Credenciales de acceso incorrectas."
            return render(request, 'login_templates/login.html', { 'error':True,'mensaje': mensaje})

    def get(self,request):
        return render(request, 'login_templates/login.html',)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('userLogin'))

@login_required
def generaMapa(request,year):
    obj=[]
    liste={}
    año=int(year)
    result=AsuntoArea.objects.prefetch_related('area')
    todasLasAreas=obtenSubareas(request.user.area.pk)
    return render(request, 'archivoDgtl/map.html',{'mapa':result,'areas':todasLasAreas})

class archivoDigitalView(LoginRequiredMixin,ListView):
    template_name = "archivoDgtl/archivoDigital.html"
    login_url = "../"
    redirect_field_name = ''
    paginate_by = 100

    def dispatch(self, request, *args, **kwargs):
        self.request.session=request.session
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        fisgon=False
        busca=self.request.GET.get('busca',None)
        año=self.request.GET.get('anios',None)
        subarea=self.request.GET.get('subareas',None)
        asunto=self.request.GET.get('asuntos',None)
        if año == None or año == "0" or año == "":
            año=PeriodoGestion.objects.get(periodo='2015')
        if subarea == None or subarea == "0" or subarea == "":
            subarea = self.request.user.area.pk
            areaConsulta = Area.objects.get(pk=int(subarea))
        else:
            cantacces=False
            areaConsulta = Area.objects.get(pk=int(subarea))
            areaDeUsuario = Area.objects.get(pk=self.request.user.area.pk)
            check=obtenSubareas(areaDeUsuario.pk)

            if areaConsulta != areaDeUsuario:
                if not areaConsulta in check:
                    cantacces=True

            if areaConsulta.prioridad > areaDeUsuario.prioridad or cantacces:
                fisgon=True

        if fisgon or (areaConsulta.area_restringida and str(subarea) not in self.request.session['areasUnrestricted']):
            new_context = []
        else:
            if asunto != None and asunto != "0" and asunto != "":
                asunto=int(asunto)
                if busca != None and busca != "":
                    new_context = Documento.objects.filter(
                        periodo=año,area=subarea,asunto=asunto,documento__icontains=busca
                    ).order_by('documento')
                else:
                    new_context = Documento.objects.filter(
                        periodo=año,area=subarea,asunto=asunto
                    ).order_by('documento')
            else:
                if busca != None and busca != "":
                    new_context = Documento.objects.filter(
                        periodo=año,area=subarea,asunto=None,documento__icontains=busca
                    ).order_by('documento')
                else:
                    new_context = Documento.objects.filter(
                        periodo=año,area=subarea,asunto=None
                    ).order_by('documento')
        return new_context

    def get_context_data(self, **kwargs):
        fisgon=False
        context = super(archivoDigitalView, self).get_context_data(**kwargs)
        año=self.request.GET.get('anios',None)
        subarea=self.request.GET.get('subareas',None)
        asunto=self.request.GET.get('asuntos',None)
        docum=self.request.GET.get('doc',None)
        if año != None and año != "0" and año != "":
            año=context['selectedaño'] = int(año)
        else:
            año=PeriodoGestion.objects.get(periodo='2015')
            año=año.pk
        if subarea != None and subarea != "0" and subarea != "":
            cantacces=False
            areaConsulta = Area.objects.get(pk=int(subarea))
            areaDeUsuario = Area.objects.get(pk=self.request.user.area.pk)
            check=obtenSubareas(areaDeUsuario.pk)

            if areaConsulta != areaDeUsuario:
                if not areaConsulta in check:
                    cantacces=True

            if areaConsulta.prioridad > areaDeUsuario.prioridad or cantacces:
                fisgon=True
        else:
            subarea = self.request.user.area.pk
            areaConsulta = Area.objects.get(pk=int(subarea))

        context['selectedsubarea'] = int(subarea)

        if asunto == None or asunto == "0" or asunto == "":
            asunto = 0
        context['asunto'] = asunto
        context['selectedasunto'] = int(asunto)

        if areaConsulta.area_restringida:
            if str(subarea) not in self.request.session['areasUnrestricted']:
                self.request.session['areaRestringida']=True

            context['anio']=año
            context['subarea']=subarea

            if str(subarea) in self.request.session['areasUnrestricted']:
                self.request.session['unrestricted']=True
            else:
                self.request.session['unrestricted']=False

        if fisgon:
            context['alertaDefisgon']=True
        context['area'] = obtenArea(subarea)
        context['subareas'] = obtenSubareas(self.request.user.area.pk)
        context['años'] = PeriodoGestion.objects.all()
        context['asuntos']=obtenAsuntos(año,subarea,asunto)
        area=Area.objects.get(pk=int(subarea))

        if fisgon:
            context['ruta']=[]
        else:
            context['ruta']=retornaBreadCumbAreas(area,[])
        if asunto == 0:
            context['rutaAsunto']=[]
        else:
            if fisgon:
                context['rutaAsunto']=[]
            else:
                asu=AsuntoArea.objects.get(pk=int(asunto),periodo=año)
                context['rutaAsunto']=retornaBreadCumbAsuntos(asu,[],año,area)
        context['usuario']=self.request.user.first_name
        context['docsUnRestricted']=self.request.session['docsUnRestricted']

        return context

def obtenArea(area):
    return Area.objects.get(pk=area)

def obtenSubareas(area):
    childs=[]
    areaInfo=Area.objects.get(pk=area)
    if areaInfo.tipo == 'Dirección':
        Direcciones=Area.objects.filter(area_superior=areaInfo.pk)
        for Direccion in Direcciones:
            childs.append(Direccion)
            Subdirecciones = Area.objects.filter(area_superior=Direccion.pk)
            if Subdirecciones.exists():
                for Subdireccion in Subdirecciones:
                    childs.append(Subdireccion)
                    Coordinaciones = Area.objects.filter(area_superior=Subdireccion.pk)
                    if Coordinaciones.exists():
                        for Coordinacion in Coordinaciones:
                            childs.append(Coordinacion)
    elif areaInfo.tipo == 'Subdirección':
        Subdirecciones=Area.objects.filter(area_superior=areaInfo.pk)
        if Subdirecciones.exists():
            for Subdireccion in Subdirecciones:
                childs.append(Subdireccion)
                Coordinaciones = Area.objects.filter(area_superior=Subdireccion.pk)
                if Coordinaciones.exists():
                    for Coordinacion in Coordinaciones:
                        childs.append(Coordinacion)
    elif areaInfo.tipo == 'Coordinación/Jefatura':
        Coordinaciones=Area.objects.filter(area_superior=areaInfo.pk)
        if Coordinaciones.exists():
            for Coordinacion in Coordinaciones:
                childs.append(Coordinacion)
    return childs

def checkRestrict(request):
    print('check restrict')
    area=request.POST.get('subareas')
    anios=request.POST.get('anios')
    areaRestringida = Area.objects.get(pk=int(area))
    areaRestrict = AreaRestringida.objects.get(area=areaRestringida)
    passwordArea=request.POST.get('passwordAreaRestricted')
    if check_password(passwordArea, areaRestrict.password):
        request.session['intentos']=0
        if area not in request.session['areasUnrestricted']:
            request.session['unrestricted']=True
            request.session['areaRestringida']=False
            lista=request.session['areasUnrestricted']
            lista.append(area)
            request.session['areasUnrestricted']=lista
        return redirect(reverse('archivoDigital') + '?anios={}&subareas={}&asuntos={}'.format(anios,area,0))
    else:
        if request.session['intentos']<2:
            request.session['intentos']=request.session['intentos']+1
            print('incrementa intentos')
            return redirect(reverse('archivoDigital') + '?anios={}&subareas={}&asuntos={}'.format(anios,area,0))
        else:
            request.user.is_active=False
            request.user.save()
            sender(3,request.user.email,'Usuario Bloqueado','','')
            incidencia=ReporteInsidencias(hora=datetime.datetime.now(),usuario=request.user,causa='Intento de acceso al area {}'.format(area))
            incidencia.save();
            logout(request)
            return HttpResponseRedirect(reverse('userLogin'))

def checkRestrictDoc(request):
    area=request.POST.get('subareas')
    anios=request.POST.get('anios')
    asuntoss=request.POST.get('asuntos')
    restric=DocumentoRestringido.objects.get(periodo=anios,area=area)
    iddoc=request.POST.get('documentoR')
    passwordDoc=request.POST.get('pasdoc')
    if check_password(passwordDoc, restric.password):
        request.session['intentosDoc']=0
        doc=Documento.objects.get(pk=int(iddoc))
        if iddoc not in request.session['docsUnRestricted']:
            lista=request.session['docsUnRestricted']
            lista.append(int(iddoc))
            request.session['docsUnRestricted']=lista
            print(type(request.session['docsUnRestricted'][0]))
        return redirect(reverse('archivoDigital') + '?anios={}&subareas={}&asuntos={}'.format(anios,area,asuntoss))
    else:
        if request.session['intentosDoc']<2:
            request.session['intentosDoc']=request.session['intentosDoc']+1
            return redirect(reverse('archivoDigital') + '?anios={}&subareas={}&asuntos={}'.format(anios,area,asuntoss))
        else:
            request.user.is_active=False
            request.user.save()
            sender(3,request.user.email,'Usuario Bloqueado','','')
            logout(request)
            return HttpResponseRedirect(reverse('userLogin'))

def obtenArea(area):
    return Area.objects.get(pk=area)

def obtenSubareas(area):
    childs=[]
    areaInfo=Area.objects.get(pk=area)
    if areaInfo.tipo == 'Dirección':
        Direcciones=Area.objects.filter(area_superior=areaInfo.pk)
        for Direccion in Direcciones:
            childs.append(Direccion)
            Subdirecciones = Area.objects.filter(area_superior=Direccion.pk)
            if Subdirecciones.exists():
                for Subdireccion in Subdirecciones:
                    childs.append(Subdireccion)
                    Coordinaciones = Area.objects.filter(area_superior=Subdireccion.pk)
                    if Coordinaciones.exists():
                        for Coordinacion in Coordinaciones:
                            childs.append(Coordinacion)
    elif areaInfo.tipo == 'Subdirección':
        Subdirecciones=Area.objects.filter(area_superior=areaInfo.pk)
        if Subdirecciones.exists():
            for Subdireccion in Subdirecciones:
                childs.append(Subdireccion)
                Coordinaciones = Area.objects.filter(area_superior=Subdireccion.pk)
                if Coordinaciones.exists():
                    for Coordinacion in Coordinaciones:
                        childs.append(Coordinacion)
    elif areaInfo.tipo == 'Coordinación/Jefatura':
        Coordinaciones=Area.objects.filter(area_superior=areaInfo.pk)
        if Coordinaciones.exists():
            for Coordinacion in Coordinaciones:
                childs.append(Coordinacion)
    return childs

def obtenAsuntos(año,area,asuntoPadre):
    if asuntoPadre==0:
        asuntos = AsuntoArea.objects.filter(area=area,periodo=año)
        if asuntos.exists():
            return asuntos
        else:
            return AsuntoArea.objects.none()
    else:
        asuntos = AsuntoArea.objects.filter(area=area,periodo=año,asuntoPadre=asuntoPadre)
        if asuntos.exists():
            return asuntos
        else:
            return AsuntoArea.objects.none()

def retornaBreadCumbAreas(area,ar):
    if area.clave != 'DG':
        areaArriba=Area.objects.get(nombre=area.area_superior)
        ar.append(area)
        return retornaBreadCumbAreas(areaArriba,ar)
    else:
        ar.append(area)
        return ar

def retornaBreadCumbAsuntos(asunto,ar,año,area):
    if AsuntoArea.objects.filter(pk=asunto.pk,periodo=año,area=area.pk).exists():
        if asunto.nivel != 1:
            asuntoArriba=AsuntoArea.objects.get(nombre=asunto.asuntoPadre,periodo=año,pk=asunto.asuntoPadre.pk)
            ar.append(asunto)
            return retornaBreadCumbAsuntos(asuntoArriba,ar,año,area)
        else:
            ar.append(asunto)
            return ar
    else:
        return []


def load_asunto(request):
    area = request.GET.get('area')
    options = '<option value="" selected="selected">---------</option>'

    if area:
        asuntos = AsuntoArea.objects.filter(area=area).order_by('Nombre')
    for asunt in asuntos :
        options+='<option value="%s">%s</option>' % (
            asunt.pk,
            asunt.Nombre
        )
    response = {}
    response['asuntos'] = options
    return JsonResponse(response)
