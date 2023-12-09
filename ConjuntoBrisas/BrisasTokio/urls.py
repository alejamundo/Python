
from django.contrib import admin
from django.urls import path
#aca traemos todas las views que renderizan cada una de las paginas
from webapp.views import index ,zonascomunes,registroresidentes,registroinmuebles,registrovisitantes,obtener_residentes_autorizados,reservas,pqrss,registroencargados,registrovehiculos,procesarpqrs,procesar_pqr,obtener_detalle_pqr,listadoreservas,listadopqrs,listadoinmuebles

urlpatterns = [
    path('admin/', admin.site.urls),

    #Página de inicio
    path('', index,name='index'),

    #Páginas de Reservas y de creación de zonas comunes
    path('zonascomunes/', zonascomunes, name='zonascomunes'),
    path('reservas/', reservas, name='reservas'),

    #Páginas para registros
    path('registroresidentes/', registroresidentes, name='registroresidentes'),
    path('registroinmuebles/', registroinmuebles, name='registroinmuebles'),
    path('registrovisitantes/', registrovisitantes, name='registrovisitantes'),
    path('obtener_residentes_autorizados/<int:apartamento_id>/', obtener_residentes_autorizados, name='obtener_residentes_autorizados'),
    path('registroencargados/', registroencargados, name='registroencargados'),
    path('registrovehiculos/', registrovehiculos, name='registrovehiculos'),

    #Páginas para la gestion de pqrsd 
    path('pqrs/', pqrss, name='pqrs'),
    path('procesarpqrs/', procesarpqrs, name='procesarpqrs'),
    path('procesar_pqr/<int:pqr_id>/', procesar_pqr, name='procesar_pqr'),
    path('obtener_detalle_pqr/<int:pqr_id>/', obtener_detalle_pqr, name='obtener_detalle_pqr'),

    #Páginas para los listados es decir los informes
    path('listadoreservas/', listadoreservas, name='listadoreservas'),
    path('listadopqrs/', listadopqrs, name='listadopqrs'),
    path('listadoinmuebles/', listadoinmuebles, name='listadoinmuebles'),



]

    
  