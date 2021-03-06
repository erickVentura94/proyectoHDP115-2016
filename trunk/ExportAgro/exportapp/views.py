from django.shortcuts import render
from masivo import masivo
from exportapp.models import pais,formula,mes,tipo_producto,producto,temporada,informacion_exportacion
# Create your views here.
from django.http import Http404
from django import forms
from django.db.models import Sum,Avg,Max
from django.views.generic import ListView
from django.template.context_processors import request
from django.contrib import messages
from audioop import avg
from telnetlib import theNULL
import csv
from __builtin__ import enumerate, all
from httplib import HTTP
from django.http import HttpResponse
from django.http.response import Http404
from zeitgeist.datamodel import NULL_EVENT

masivos=masivo()
def ingresarindividual(request):
    paises=pais.objects.all()
    anios=temporada.objects.all()
    meses=mes.objects.all()
    tipos=tipo_producto.objects.all()
    productos=producto.objects.all()
    context={
             'paises':paises,
             'anios':anios,
             'meses':meses,
             'tipos':tipos,
             'productos':productos
             
             }
    
    return render(request,'ingresarindividual.html',context)
def registrarindividual(request):
    costo=request.POST.get('costo')
    peso=request.POST.get('peso')
    anio=request.POST.get('anio')
    mes_elegido=request.POST.get('mes')
    temporada_elegida=temporada.objects.get(anio=anio,numero_mes=mes_elegido).id
    producto_elegido=request.POST.get('producto')
    pais_elegido=request.POST.get('pais')
    exportacion=informacion_exportacion(codigo_producto_id=producto_elegido,codigo_temporada_id=temporada_elegida,codigo_pais_id=pais_elegido,costo_mercancia=costo,peso_kilogramos=peso)
    exportacion.save()
    paises=pais.objects.all()
    anios=temporada.objects.all()
    meses=mes.objects.all()
    tipos=tipo_producto.objects.all()
    productos=producto.objects.all()
    context={
             'paises':paises,
             'anios':anios,
             'meses':meses,
             'tipos':tipos,
             'productos':productos,
             'mensaje':"Producto agregado exitosamente"
             }
    
    return render(request,'ingresarindividual.html',context)
def editarformula(request):
    context={
             'actual':formula.objects.get(id=1).coeficiente
             }
    return render(request,'editarformula.html',context)
def registrarvalor(request):
    valor=request.POST.get('valor')
    actual=formula.objects.get(id=1)
    actual.coeficiente=int(valor)
    actual.save()
    context={
             'actual':formula.objects.get(id=1).coeficiente
                         }
    return (request,'editarformula.html',context)
def index_administrador(response):
    suma=informacion_exportacion.objects.values('codigo_producto__tipo_producto__nombre_tipo').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    sumaa=informacion_exportacion.objects.values('codigo_pais__nombre_pais').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    return render(request,'index_administrador',{'suma0':suma[0],'suma1':suma[1],'suma2':suma[2],'suma3':suma[3],'suma4':suma[4],'suma5':suma[5],'suma6':suma[6],'suma7':suma[7],'suma8':suma[8],'suma9':suma[9],'sumaa0':sumaa[0],'sumaa1':sumaa[1],'sumaa2':sumaa[2],'sumaa3':sumaa[3],'sumaa4':sumaa[4],'sumaa5':sumaa[5],'sumaa6':sumaa[6],'sumaa7':sumaa[7],'sumaa8':sumaa[8],'sumaa9':sumaa[9]})


def inicio(request):
    suma=informacion_exportacion.objects.values('codigo_producto__tipo_producto__nombre_tipo').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    sumaa=informacion_exportacion.objects.values('codigo_pais__nombre_pais').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    
    return render(request,'index.html',{'suma0':suma[0],'suma1':suma[1],'suma2':suma[2],'suma3':suma[3],'suma4':suma[4],'suma5':suma[5],'suma6':suma[6],'suma7':suma[7],'suma8':suma[8],'suma9':suma[9],'sumaa0':sumaa[0],'sumaa1':sumaa[1],'sumaa2':sumaa[2],'sumaa3':sumaa[3],'sumaa4':sumaa[4],'sumaa5':sumaa[5],'sumaa6':sumaa[6],'sumaa7':sumaa[7],'sumaa8':sumaa[8],'sumaa9':sumaa[9]})

def modificar(request):
    meses=mes.objects.all()
    temporadas=temporada.objects.all()
    paises=pais.objects.all().order_by('nombre_pais')
    tipo_productos=tipo_producto.objects.all().order_by('nombre_tipo')
    x=informacion_exportacion.objects.all().aggregate(Max('id'))
    
    context= {'meses':meses,
             'temporadas':temporadas,
              'paises':paises,
              'tipo_productos':tipo_productos
          
        
             }
             
            
    exportaciones1=informacion_exportacion.objects.all()
    return render(request,'modificarExportacion.html',context)

def consultarmodifica(request):
    paises=pais.objects.all().order_by('nombre_pais')
    meses=mes.objects.all()
    temporadas=temporada.objects.all()
    tipo_productos=tipo_producto.objects.all().order_by('nombre_tipo')
    productos=producto.objects.all()
    productos1=producto.objects.values("codigo_arancelario").order_by()
    
    
    producto_elegido=request.POST.get('producto')
    pais_elegido=request.POST.get('pais')
    mes_elegido=request.POST.get('mes')
    anio_elegido=request.POST.get('anio')
    
    if((pais_elegido=="todos" )& (mes_elegido=="todos")) :
        
     
     exportaciones_elegidas=informacion_exportacion.objects.values('id','codigo_producto_id__nombre_producto','codigo_temporada_id__anio','codigo_pais_id__nombre_pais','codigo_temporada_id__numero_mes_id__nombre_mes','costo_mercancia','peso_kilogramos','codigo_producto_id__procesado').filter(codigo_producto_id__tipo_producto_id__nombre_tipo=producto_elegido).filter(codigo_temporada_id__anio=anio_elegido)
    elif(pais_elegido=="todos") & (mes_elegido != "todos") :
         exportaciones_elegidas=informacion_exportacion.objects.values('id','codigo_producto_id__nombre_producto','codigo_temporada_id__anio','codigo_pais_id__nombre_pais','codigo_temporada_id__numero_mes_id__nombre_mes','costo_mercancia','peso_kilogramos','codigo_producto_id__procesado').filter(codigo_producto_id__tipo_producto_id__nombre_tipo=producto_elegido).filter(codigo_temporada_id__anio=anio_elegido).filter(codigo_temporada_id__numero_mes_id__nombre_mes=mes_elegido)

    elif(pais_elegido !="todos") & (mes_elegido=="todos"):
        exportaciones_elegidas=informacion_exportacion.objects.values('id','codigo_producto_id__nombre_producto','codigo_temporada_id__anio','codigo_pais_id__nombre_pais','codigo_temporada_id__numero_mes_id__nombre_mes','costo_mercancia','peso_kilogramos','codigo_producto_id__procesado').filter(codigo_producto_id__tipo_producto_id__nombre_tipo=producto_elegido).filter(codigo_temporada_id__anio=anio_elegido).filter(codigo_pais_id__nombre_pais=pais_elegido)
    else:
       exportaciones_elegidas=informacion_exportacion.objects.values('id','codigo_producto_id__nombre_producto','codigo_temporada_id__anio','codigo_pais_id__nombre_pais','codigo_temporada_id__numero_mes_id__nombre_mes','costo_mercancia','peso_kilogramos','codigo_producto_id__procesado').filter(codigo_producto_id__tipo_producto_id__nombre_tipo=producto_elegido).filter(codigo_temporada_id__anio=anio_elegido).filter(codigo_temporada_id__numero_mes_id__nombre_mes=mes_elegido).filter(codigo_pais_id__nombre_pais=pais_elegido) 
    
     
    
    
    context= {'paises':paises,
              'meses':meses,
              'temporadas':temporadas,
              'tipo_productos': tipo_productos,
              'productos':productos1,
              'exportaciones':exportaciones_elegidas,
              'producto_elegido':producto_elegido,
              'anio_elegido':anio_elegido
              }
    
    
    return render(request,'modificarExportacion.html',context)

def eliminar(request,id):
    
    informacion_exportacion.objects.get(id=id).delete()
    
    return render(request,'cambiarexportacion.html')
def modificarexportacion(request,id):
    exportacion=informacion_exportacion.objects.get(id=id)
    nombre_producto=producto.objects.get(codigo_arancelario=exportacion.codigo_producto_id)
    nombre_pais=pais.objects.get(id=exportacion.codigo_pais_id)
    valor=exportacion.costo_mercancia
    peso=exportacion.peso_kilogramos
    tipo_productos=tipo_producto.objects.get(id=nombre_producto.tipo_producto_id)
    
    context={
             
             'exportacion':exportacion,
             'nombre_producto':nombre_producto,
             'nombre_pais':nombre_pais,
             'valor':valor,
             'peso':peso,
             'tipo_producto':tipo_productos
             }
    
    
    return render(request,'cambiarexportacion.html',context)


def actualizar_exportacion(request,id):
        exportacion=informacion_exportacion.objects.get(id=id)
        
        if request.POST.get('valor') != "#####":
                exportacion.costo_mercancia=request.POST.get('valor')
                exportacion.save()
        if request.POST.get('peso') != "#####" :
                exportacion.peso_kilogramos=request.POST.get('peso')
                exportacion.save()
        
    
        return modificar(request)

## lo de abajo hay que borrarlo esto era una prueba

def sesion(request):
       return render(request, 'iniciar_sesion.html')
   ######################insercion masiva###############################################
def ingresarmasivo(request):
    
    return render(request,'insertarmasivamente.html')
       




def validar(request):
    exportacionesmasivas=[]
    masivos.productos=[]
    cadena = "Errores:"
    ruta=request.POST.get('rutas')
    reader=csv.reader(open('entradasmasivas/'+ruta,'r'))
    for index,row in enumerate(reader):
        if validar_entrada(row[0],row[1],row[2],row[3],row[4],row[5]):
           exportacionesmasivas.append([row[0],row[1],row[2],row[3],row[4],row[5],index])
           masivos.productos.append([row[0],row[1],row[2],row[3],row[4],row[5]])
        else:
            cadena=cadena+"\nerror en :"+"Fila:"+str(index)+"Fila no se mostrara para su insercion"
        
    context={
             'exportaciones':exportacionesmasivas,
             'tamanio':len(exportacionesmasivas),
             'errores':cadena,
             
                         }
    
    return render(request,'visualizar_entradas_masivas.html',context)
   
##funcion para validar entradas masivas   
def validar_entrada(codigo,peso,valor,pais_elegido,mes_elegido,anio_elegido):
    validar=True
    try:
        esquema=len(producto.objects.all().filter(codigo_arancelario=codigo))
        if esquema==0:
            validar=False
        
    except ValueError:
     validar= False
    
    try:
        esquema1=len(pais.objects.all().filter(nombre_pais=pais_elegido))
        if esquema1==0:
            validar=False
    except ValueError:
        validar= False
 
    try:
         esquema2=len(mes.objects.all().filter(nombre_mes=mes_elegido))
         if esquema2==0:
             validar=False
    except ValueError:
         validar= False
    try:
         esquema3=len(temporada.objects.all().filter(anio=anio_elegido))
         if esquema3==0:
             validar=False
    except ValueError:
         validar= False
    return validar
##ingresar valores#####################################
def ingresar_datos(request):
    for informacion in masivos.productos:
        pais_elegido=pais.objects.get(nombre_pais=informacion[3]).id
        temporada_elegida=(temporada.objects.filter(anio=informacion[5]).filter(numero_mes_id__nombre_mes=informacion[4]))[0].id
        export=informacion_exportacion(codigo_producto_id=informacion[0],codigo_temporada_id=temporada_elegida,peso_kilogramos=float(informacion[2]),costo_mercancia=float(informacion[1]),codigo_pais_id=int(pais_elegido))
        export.save()
       
        
        
    return render(request,'exito_exportacion_masiva.html',{'tamanio':len(masivos.productos)})
######################################################


################################hasta aca la insercion masiva#################


def busqueda(request):
    elegir_pais=request.POST['pais']
    elegir_producto=request.POST['producto']
    elegir_mes_s=request.POST['mes']
    elegir_anio=request.POST['anio']
    
    
    informacion_exportaciones=informacion_exportacion.objects.filter(id=1)
    
    context={
                         'exportaciones':informacion_exportaciones
                         }                

    return render(request,'prueba.html',context)

def top10(request):
    suma=informacion_exportacion.objects.values('codigo_producto__tipo_producto__nombre_tipo').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    sumaa=informacion_exportacion.objects.values('codigo_pais__nombre_pais').annotate(suma=Sum('costo_mercancia')).order_by('-suma')[:10]
    return render(request,'index_administrador.html',{'suma0':suma[0],'suma1':suma[1],'suma2':suma[2],'suma3':suma[3],'suma4':suma[4],'suma5':suma[5],'suma6':suma[6],'suma7':suma[7],'suma8':suma[8],'suma9':suma[9],'sumaa0':sumaa[0],'sumaa1':sumaa[1],'sumaa2':sumaa[2],'sumaa3':sumaa[3],'sumaa4':sumaa[4],'sumaa5':sumaa[5],'sumaa6':sumaa[6],'sumaa7':sumaa[7],'sumaa8':sumaa[8],'sumaa9':sumaa[9]})

def iniciar_sesion(request):
    
    return render(request,'iniciar_sesion.html')
####################################consultar por tipo de producto#
def consultar_exportacion(request):
        context={
                'tipo_producto':tipo_producto.objects.all().order_by('nombre_tipo')
                }
        return render(request,'consultar_exportacion.html', context)
def realizar_consulta(request):
    producto=int(request.POST.get('producto'))
    tipo=tipo_producto.objects.get(id=producto)
    
    export_temporada=informacion_exportacion.objects.filter(codigo_producto_id__tipo_producto_id=tipo).values('codigo_temporada_id__numero_mes_id__nombre_mes').annotate(suma=Sum('costo_mercancia')).order_by('codigo_temporada')[:12]
    pivote=formula.objects.get(id=1)
    valor=pivote.coeficiente
    costo_pronostico=0
    for i in range(valor):
        aux=export_temporada[i]
        costo_pronostico=costo_pronostico+aux['suma']
    promedio=costo_pronostico/valor
    
    
    
    context={
             'tipo_producto':tipo_producto.objects.all().order_by('nombre_tipo'),
             'suma0': export_temporada[0],
             'suma1': export_temporada[1],  
             'suma2': export_temporada[2],  
             'suma3': export_temporada[3],  
             'suma4': export_temporada[4],  
             'suma5': export_temporada[5],  
             'suma6': export_temporada[6],  
             'suma7': export_temporada[7],  
             'suma8': export_temporada[8],  
             'suma9': export_temporada[9],  
             'suma10': export_temporada[10],  
             'suma11': export_temporada[11],    
             'promedio':promedio
             }
    return render(request,'consultar_exportacion.html',context)
#####################finaliza consulta##################

        
