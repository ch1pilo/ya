from django.db import models
from django.conf import settings

# Create your models here.

class TipoUser(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipoUser = models.CharField(max_length=30)
    
class postulado(models.Model):
    Nombres = models.CharField(max_length=30)
    Apellidos = models.CharField(max_length=30)
    Cedula_P = models.CharField(max_length=8)
    Fechanacimiento = models.DateField(null=False)
    GrupoEtnico = models.CharField(max_length=30)
    N_TLF = models.CharField(max_length=12)
    Direccion = models.CharField(max_length=100)
    CorreoE= models.CharField(max_length=30)
    Fecha_postulacion = models.DateTimeField(auto_now_add=True)
    estatus = models.TextField(max_length=10)

class Facultad(models.Model):
    facult = models.CharField(max_length=8)
    
class Carreras(models.Model):
    Nombre = models.CharField(max_length=20)
    facultad = models.ForeignKey(Facultad, on_delete=models.CASCADE, related_name='carreras')    
   
class ppostulador (models.Model):
    
    Nombre = models.CharField(max_length=30)
    Apellino = models.CharField(max_length=30)
    CedulaPostulador = models.CharField(max_length=9)
    
class postuladoDAcademicos(models.Model):
    idPostulado = models.OneToOneField(postulado, on_delete=models.CASCADE,  related_name='academicos')
    ColegioEgreso= models.CharField(max_length=50)
    AnoGraduacion = models.CharField(max_length=4)
    Trabaja = models.CharField(max_length=4)
    TrabajsComentario = models.CharField(max_length=100)
    EstudiosPrevios = models.CharField(max_length=4)
    ComentarioEstudios = models.CharField(max_length=100)
    
    Carrer_a_postular = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    
    idDPostulador = models.ForeignKey(ppostulador, on_delete=models.CASCADE)
    Programa = models.CharField(max_length=100)
    


class requisi (models.Model):
    idpostulado = models.OneToOneField(postulado, on_delete=models.CASCADE)
    PruebaObsu = models.CharField(max_length=11)
    TituloBachiller = models.CharField(max_length=11)
    fotoCopiaCedula = models.CharField(max_length=11)
    NotasCertificadas = models.CharField(max_length=11)
    fotos = models.CharField(max_length=11)

class EsActivo (models.Model):
    idinscrito = models.OneToOneField(postulado, on_delete=models.CASCADE)
    EstadoEstudiante = models.CharField(max_length=10)
    FechaInsc = models.DateTimeField(auto_now_add=True)


 
class Periodo(models.Model):
    par = models.CharField(max_length=10)
    perioIns = models.ForeignKey(EsActivo, on_delete=models.CASCADE)
    

    