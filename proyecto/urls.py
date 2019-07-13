"""proyecto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from archivoDigital import views
from archivoDigital.views import userLogin,archivoDigitalView
#admin.autodiscover()

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^private_files/', include('private_files.urls')),
    url(r'^$',userLogin.as_view(),name='userLogin'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^archivoDigital/',archivoDigitalView.as_view(),name='archivoDigital'),
    url(r'^checkRestrict/',views.checkRestrict,name='checkRestrict'),
    url(r'^checkRestrictDoc/',views.checkRestrictDoc,name='checkRestrictDoc'),
    url(r'^generaMapa/(?P<year>[0-9]?)/$',views.generaMapa,name='generaMapa'),
]

from django.conf import settings

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
