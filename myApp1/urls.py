from django.urls import path
from myApp1 import views
from django.contrib.auth import views as au_views

urlpatterns = [
    path('', views.viw, name='vista'),
    path('decano/', views.decano, name='decano'),
    path('aprobar/', views.aprobar, name='aprobar'),
    path('negar/', views.negar, name='negar'),
    path('requisitos/', views.requisitos, name='requisitos'),
    path('aggRe/', views.aggRe, name='aggRe'),
    path('externo/', views.externo, name='externo'),
    path('ediPerfil/', views.ediPerfil, name='ediPerfil'),
    path('actualizarUsuario/', views.actualizarUsuario, name='actualizarUsuario'),
    path('registrarUsuario/', views.registrarUsuario, name='registrarUsuario'),
    path('aggPosr/', views.aggPosr, name='aggPosr'),
    path('aggUsuario/', views.aggUsuario, name='aggUsuario'),
    path('aggPostulador/', views.aggPostulador, name='aggPostulador'),
    path('aggF/', views.aggF, name='aggF'),
    path('aggC/', views.aggC, name='aggC'),
    path('lista_facultades/', views.lista_facultades, name='lista_facultades'),
    path('listar_postulados/', views.listar_postulados, name='listar_postulados'),

    path('listarBecado/', views.listarBecado, name='listarBecado'),

    path('becados/descargar/', views.descargarBecados, name='descargarBecados'),
    path('postulados/descargar/', views.descargar_postulados, name='descargar_postulados'),
    path('reporte/', views.reporte, name='reporte'),
    path('reportePost/', views.reportePost, name='reportePost'),
    
    path('inscribir/', views.inscripcion, name='inscribir'),
    path('admi/', views.admi, name='admi'),
    path('ins/', views.ins, name='ins'),
    path('profile/', views.profile, name='prifile'),
    path('contiInsert/', views.contiInsert, name='contiInsert'),
    path('postular/', views.postular, name='postular'),
    path('lP/', views.consul, name='lP'),
    path('login/', au_views.LoginView.as_view(), name='login'),
    path('logout/', au_views.LogoutView.as_view(), name='logout'),
    path('insertar/', views.insertar, name='insertar'),
]
