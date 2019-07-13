from django.core.exceptions import PermissionDenied
from archivoDigital.models import Area
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.http import HttpResponse

def area_user_is_restricted(function):
    def wrap(request, *args, **kwargs):
        User = get_user_model()

        usuario=User.objects.get(email=request.user)
        datosArea = Area.objects.filter(Nombre=usuario.area)

        if datosArea[0].Area_Restringida:
            raise PermissionDenied
        else:
            return function(request, *args, **kwargs)
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
