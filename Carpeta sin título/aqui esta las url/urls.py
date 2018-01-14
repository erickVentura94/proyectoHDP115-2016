"""ExportAgro URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url,patterns,include
from django.contrib import admin,auth
from exportapp.views import inicio
from exportapp.views import modificar
from exportapp.views import busqueda,iniciar_sesion,consultar_exportacion,consultarmodifica,top10,eliminar,modificarexportacion,validar,actualizar_exportacion,ingresarmasivo,ingresar_datos

#from exportagro.views import sesion
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/','django.contrib.auth.views.login',{'template_name':'iniciar_sesion.html'},name='login'),
    url(r'^$',top10),
    url(r'^modifica',modificar,name='modificar'),
    
   ##consultar_exportacion 
  
   
    
    ## #########Crud Administrador ###############
    url(r'^consultamodifica/',consultarmodifica),
   url(r'^eliminar/(?P<id>[^/]+)/',eliminar),
   url(r'^cambiar/(?P<id>[^/]+)',modificarexportacion),
   url(r'^actualizar/(?P<id>[^/]+)',actualizar_exportacion),
   #################################################
  ##############ingreso individual################
  url(r'^consultar_exportacion/',consultar_exportacion),
   
   ##############ingreso masivo #####################
   
   url(r'^ingresomasivo/',ingresarmasivo),
   url(r'^verificar/',validar),     ####template 1
   
   url(r'^ingresardatos/',ingresar_datos)
#########################################################

]

