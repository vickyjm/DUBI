# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from estacionamientos import views


# Este error es raro, en django funciona
urlpatterns = patterns('',
    url(r'^$', views.estacionamientos_all, name = 'estacionamientos_all'),
    url(r'^consultarI$', views.estacionamiento_ingreso, name = 'estacionamiento_ingreso'),
    url(r'^consultarR$', views.consultar_reservas,name = 'consultar_reservas'),
    url(r'^(?P<_id>\d+)/$', views.estacionamiento_detail, name = 'estacionamiento_detail'),
    url(r'^(?P<_id>\d+)/reserva$', views.estacionamiento_reserva, name = 'estacionamiento_reserva'),
    url(r'^(?P<_id>\d+)/pagar$',views.estacionamiento_pagar_reserva, name = 'estacionamiento_pagar_reserva'),
    url(r'^(?P<_id>\d+)/ocupacion$',views.estacionamiento_tasa_ocupacion, name = 'estacionamiento_tasa_ocupacion'),
 	url(r'^(?P<_id>\d+)/tasaDia$',views.estacionamiento_tasa_ocupacion_dia, name = 'estacionamiento_tasa_ocupacion_dia'),    
 	url(r'^(?P<_id>\d+)/tasaHora$',views.estacionamiento_tasa_ocupacion_hora, name = 'estacionamiento_tasa_ocupacion_hora'),    
)
