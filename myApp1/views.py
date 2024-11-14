import csv
from tkinter import simpledialog
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from myApp1.models import Carreras, EsActivo, Facultad, TipoUser, postulado, postuladoDAcademicos, ppostulador, requisi

def viw(request):
    return render(request, "index.html")

@login_required
def decano(request):
    try:
        tipo_usuario = TipoUser.objects.get(user=request.user)
        if tipo_usuario.tipoUser == 'decano':
            return render(request, "decano.html")
    except TipoUser.DoesNotExist:
        messages.error(request, "Tipo de usuario no encontrado.")
    return render(request, "index.html")

@login_required
def externo(request):
    try:
        tipo_usuario = TipoUser.objects.get(user=request.user)
        if tipo_usuario.tipoUser == "externo":
            return render(request, "externos.html")
    except TipoUser.DoesNotExist:
        messages.error(request, "Tipo de usuario no encontrado.")
    return render(request, "index.html")

@login_required
def ins(request):
    try:
        tipo_usuario = TipoUser.objects.get(user=request.user)
        if tipo_usuario.tipoUser == "ins":
            return render(request, "inscripcion.html")
    except TipoUser.DoesNotExist:
        messages.error(request, "Tipo de usuario no encontrado.")
    return render(request, "index.html")

@login_required
def profile(request):
    try:
        tipo_usuario = TipoUser.objects.get(user=request.user)
        username = tipo_usuario.tipoUser
        if username == 'decano':
            return redirect("decano")
        elif username == "":
            return redirect("admi")
        elif username == 'ins':
            return redirect("ins")
        elif username == "externo":
            return redirect('externo')
        else:
            messages.success(request, '¡Usuario no encontrado!')
            return redirect('login')
    except TipoUser.DoesNotExist:
        messages.error(request, "Tipo de usuario no encontrado.")
        return redirect('login')

@login_required
def admi(request):
    try:
        tipo_usuario = TipoUser.objects.get(user=request.user)
        if tipo_usuario.tipoUser == '' or tipo_usuario.tipoUser == "admi":
            return render(request, "admin.html")
    except TipoUser.DoesNotExist:
        messages.error(request, "Tipo de usuario no encontrado.")
        return redirect('login')

    messages.info(request, "Acceso denegado. No tienes permiso para acceder a esta página.")
    return render(request, "index.html")  
    
@login_required
def postular (request):
    return render(request, "postular.html")



@login_required
def ediPerfil (request):
    return render(request, "ediPerfil.html")

@login_required
def reporte(request):
    postulados = postulado.objects.all()
    dic = {'pos':postulados}
    return render(request, 'reportes.html', dic)

@login_required
def reportePost (request):
    nom = request.POST['nombre']
    ape = request.POST['apellido']
    
    id = request.POST['id']
    idd = int(id)
    dPers = postulado.objects.all()
    dAca = postuladoDAcademicos.objects.all()
    requi = requisi.objects.all()
    carrera = Carreras.objects.all()
    dic = {
        'car':carrera,
       'id':idd,
       'dp':dPers,
       'da':dAca,
       're':requi,
       'nom':nom,
       'ape':ape
    }
    return render(request, "datosPos.html", dic)
    
@login_required
def insertar(request):
    if request.method == 'POST':
        # Obtener todos los registros de postulados
        todos = postulado.objects.all()
        cedu = request.POST.get('cedula', "").strip()
        
        # Si no hay registros, no hay duplicados
        if not todos:
            # Proceder a guardar el nuevo registro directamente
            enviar = postulado(
                Nombres=request.POST['nombre'],
                Apellidos=request.POST['apellido'],
                Cedula_P=cedu,
                Fechanacimiento=request.POST['fecha'],
                GrupoEtnico=request.POST['etnia'],
                N_TLF=request.POST['tlf'],
                Direccion=request.POST['direccion'],
                CorreoE=request.POST['correo'],
                estatus='pendiente'
            )
            enviar.save()

            # Obtener el ID del nuevo registro
            idAgg = enviar.id
            objetoPostu = ppostulador.objects.all()
            facultades = Facultad.objects.all()
            carreras = Carreras.objects.all()
            # Preparar los datos para la plantilla
            datos = {
                'r': 'Registrado correctamente',
                'id': idAgg,
                'postu': objetoPostu,
                'facul':facultades,
                'car' : carreras
            }
            return render(request, "continuar.html", datos)

        # Comprobar si la cédula ya existe
        if any(i.Cedula_P == cedu for i in todos):
            dt= {'r' : "Cédula duplicada"}
            return render(request, 'postular.html', dt)

        # Si la cédula no está duplicada, proceder a guardar el nuevo registro
        enviar = postulado(
            Nombres=request.POST['nombre'],
            Apellidos=request.POST['apellido'],
            Cedula_P=cedu,
            Fechanacimiento=request.POST['fecha'],
            GrupoEtnico=request.POST['etnia'],
            N_TLF=request.POST['tlf'],
            Direccion=request.POST['direccion'],
            CorreoE=request.POST['correo'],
            estatus='pendiente'
        )
        enviar.save()

        # Obtener el ID del nuevo registro
        idAgg = enviar.id
        objetoPostu = ppostulador.objects.all()
        facultades = Facultad.objects.all()
        carreras = {facultad.id: facultad.carreras.all() for facultad in facultades}
        # Preparar los datos para la plantilla
        datos = {
            'r': 'Registrado correctamente',
            'id': idAgg,
            'postu': objetoPostu,
            'facul': facultades, 
            'carreras': carreras
        }
        return render(request, "continuar.html", datos)

    # Si no es un método POST, renderizar la plantilla de postulación
    datos = {'r2': 'Presione el botón para guardar'}
    return render(request, "postular.html", datos)
    
def contiInsert (request):
    idd = request.POST['id']
    iddd = int(idd)
    idp = request.POST['idp']
    idpp = int(idp)
    postulado_obj = postulado.objects.get(id=iddd)
    escomen = request.POST['comen1']
    carrera = request.POST.get('carrera')
    di = int(carrera)
    idcar= Carreras.objects.get(id = di)
    postuObj = ppostulador.objects.get(id=idpp)
    
    enviar = postuladoDAcademicos(ColegioEgreso = request.POST['colegio'],
                                  idDPostulador = postuObj,
                                  idPostulado=postulado_obj,
                                  AnoGraduacion = request.POST['an'],
                                  Trabaja =  request.POST['traba'],
                                  TrabajsComentario = escomen,
                                  EstudiosPrevios = request.POST['estu'],
                                  ComentarioEstudios = request.POST['comen'],
                                  Carrer_a_postular = idcar,
                                  Programa = request.POST['progra']
                                  )
    enviar.save()
    return redirect("prifile")

    
@login_required
def consul (request):
    p = ppostulador.objects.all()
    postulados = postulado.objects.all()
    acade = postuladoDAcademicos.objects.all()
    
    return render(request, 'index4.html', {'pos': postulados,
                                           'all' : p,
                                           'ac' : acade
                                           })




@login_required
def inscripcion (request):
    postulados = postulado.objects.all()
    return render(request, 'insPostu.html', {'pos': postulados})

@login_required
def aprobar (request):
    idd = request.POST['id']
    postu = postulado.objects.get(id= idd)
    postu.estatus = 'aprobado'
    postu.save()
    
    enviar = requisi(idpostulado = postu,
                     PruebaObsu = "pendiente",
                     TituloBachiller = "pendiente",
                     fotoCopiaCedula = "pendiente",
                     NotasCertificadas = "pendiente",
                     fotos = "pendiente"
                     )
    enviar.save()
    return redirect("lP")

@login_required
def negar (request):
    idd = request.POST['id']
    postu = postulado.objects.get(id= idd)
    postu.estatus = 'negada'
    postu.save()
    return redirect("lP")

@login_required
def requisitos(request):
    if request.user.tipoUser == 'ins':
        id = request.POST['id']
        nom = request.POST['nombre']
        ape = request.POST['apellido']
        
        po = requisi.objects.get(idpostulado=id)
        enviar = {
                'id': id,
                'nom': nom,
                'ape': ape,
                'po' : po.PruebaObsu,
                'tb':po.TituloBachiller,
                'fc': po.fotoCopiaCedula,
                'nc': po.NotasCertificadas,
                'ft': po.fotos
                
        }
        return render(request, "requisitos.html", enviar)

@login_required
def aggRe(request):
     if request.user.tipoUser == 'ins':
         if 'act' in request.POST and request.POST['act'] == 'Inscrito' :
             idd = int(request.POST['id'])
             postu = postulado.objects.get(id= idd)
             postu.estatus = "inscrito"
             enviar = EsActivo(idinscrito=postu,
                               EstadoEstudiante = "activo"
                               )
             enviar.save()
             postu.save()
             return redirect("inscribir")
         else:
             id = request.POST.get('id')
             po = requisi.objects.get(idpostulado=id)
             po.PruebaObsu = request.POST['pO']
             po.TituloBachiller = request.POST['tb']
             po.fotoCopiaCedula = request.POST['cc']
             po.NotasCertificadas = request.POST['nc']
             po.fotos = request.POST['ftc']
             po.save()
             return redirect('inscribir')

@login_required
def aggPosr(request):
    return render(request, "nuevopostu.html")

@login_required
def aggPostulador(request):
    if request.method == 'POST':
        enviar =  ppostulador(
            Nombre = request.POST['username'],
            Apellino = request.POST['ape'],
            CedulaPostulador = request.POST['ced'],
        )
        enviar.save()
        return redirect('profile')

@login_required
def actualizarUsuario(request):
    if request.method == 'POST':
        user = request.user  # Obtén el usuario autenticado directamente
        
        # Actualiza los campos
        user.username = request.POST.get('usuarioNuevo', user.username)
        user.first_name = request.POST.get('nombre', user.first_name)
        user.last_name = request.POST.get('apellido', user.last_name)
        user.email = request.POST.get('correo', user.email)

        # Solo actualiza la contraseña si se proporciona
        if request.POST["contrasena"] != "":
            if request.POST.get('contrasena'):
                user.set_password(request.POST['contrasena'])  # Usa set_password para encriptar la contraseña 
            
        user.save()  # Guarda los cambios
        messages.success(request, 'Usuario actualizado con éxito.')  # Mensaje de éxito
        return redirect('profile')  # Asegúrate de que 'profile' sea el nombre correcto de tu vista

    return render(request, 'actualizarUsuario.html')  # Renderiza tu plantilla si no es un POST

User = get_user_model()

@login_required
def registrarUsuario (request):
    return render(request, "registrarUsuario.html")

@login_required
def aggUsuario(request):
    if request.method == 'POST':
        # Verifica si el nombre de usuario ya existe
        if User.objects.filter(username=request.POST['username']).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('registrarUsuario')

        # Crea una instancia del usuario
        user = User(
            username=request.POST['username'],
            email=request.POST['email']
        )
        
        # Establece la contraseña de forma segura
        user.set_password(request.POST['password'])
        
        # Guarda el usuario en la base de datos
        user.save()
        
        # Crea una instancia de TipoUser para el nuevo usuario
        tipo_usuario = TipoUser(user=user, tipoUser=request.POST['tipo'])
        tipo_usuario.save()

        # Mensaje de éxito
        messages.success(request, 'Usuario agregado con éxito.')

        return redirect('profile')

@login_required
def aggF(request):
    if request.method == 'POST':
        facultad_nombre = request.POST.get('facult')
        if facultad_nombre:
            Facultad.objects.create(facult=facultad_nombre)
            messages.success(request, 'Facultad agregada con éxito.')
            return redirect('aggC')  # Redirige a la vista para agregar carrera
    return render(request, 'aggF.html')
@login_required
def aggC(request):
    if request.method == 'POST':
        facultad_id = request.POST.get('facultad_id')
        nombre_carrera = request.POST.get('nombre_carrera')
        facultad = Facultad.objects.get(id=facultad_id)

        if nombre_carrera:
            Carreras.objects.create(Nombre=nombre_carrera, facultad=facultad)
            messages.success(request, 'Carrera agregada con éxito.')
            return redirect('profile')  # Redirige a la lista de facultades

    facultades = Facultad.objects.all()
    return render(request, 'aggC.html', {'facultades': facultades})
@login_required
def lista_facultades(request):
    facultades = Facultad.objects.all()  # Obtiene todas las facultades
    return render(request, 'lista_facultades.html', {'facultades': facultades})

@login_required
def listar_postulados(request):
    estatus_seleccionado = request.GET.get('estatus', 'pendiente')
    carrera_seleccionada = request.GET.get('carrera')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar postulados por estatus
    postulados = postulado.objects.filter(estatus=estatus_seleccionado)

    # Filtrar por carrera si se selecciona
    if carrera_seleccionada:
        postulados = postulados.filter(postuladodacademicos__Carrer_a_postular__id=carrera_seleccionada)

    # Filtrar por periodo de fechas si se seleccionan
    if fecha_inicio and fecha_fin:
        postulados = postulados.filter(Fecha_postulacion__date__range=[fecha_inicio, fecha_fin])

    # Obtener todas las carreras para el filtro
    carreras = Carreras.objects.all()

    return render(request, 'listar_postulados.html', {
        'postulados': postulados,
        'estatus_seleccionado': estatus_seleccionado,
        'carrera_seleccionada': carrera_seleccionada,
        'carreras': carreras,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })


@login_required
def descargar_postulados(request):
    estatus_seleccionado = request.GET.get('estatus', 'pendiente')
    carrera_seleccionada = request.GET.get('carrera')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar postulados por estatus
    postulados = postulado.objects.filter(estatus=estatus_seleccionado)

    # Filtrar por carrera si se selecciona
    if carrera_seleccionada:
        postulados = postulados.filter(postuladoDAcademicos__Carrer_a_postular__id=carrera_seleccionada)

    # Filtrar por periodo de fechas si se seleccionan
    if fecha_inicio and fecha_fin:
        postulados = postulados.filter(Fecha_postulacion__date__range=[fecha_inicio, fecha_fin])

    # Crear la respuesta HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="postulados.csv"'

    # Crear el objeto CSV writer
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Apellido', 'Cédula', 'Carrera', 'Fecha de Postulación', 'Estatus'])  # Encabezados

    for p in postulados:
        # Acceder a los datos de postuladoDAcademicos
        try:
            academico = p.academicos  # Usa el related_name aquí
            carreras = academico.Carrer_a_postular.Nombre if academico.Carrer_a_postular else 'N/A'
        except Exception:  # Captura cualquier excepción
            carreras = 'N/A'  # En caso de que no haya relación

        # Escribir cada fila en el CSV
        writer.writerow([
            p.Nombres,
            p.Apellidos,
            p.Cedula_P,
            carreras,
            p.Fecha_postulacion.strftime('%Y-%m-%d'),
            p.estatus
        ])

    return response

@login_required
def listarBecado(request):
    carrera_seleccionada = request.GET.get('carrera')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    # Filtrar postulados que están activos
    postulados_activos = postulado.objects.filter(esactivo__EstadoEstudiante='activo')

    # Filtrar por carrera si se selecciona
    if carrera_seleccionada:
        postulados_activos = postulados_activos.filter(postuladodacademicos__Carrer_a_postular__id=carrera_seleccionada)

    # Filtrar por periodo de fechas si se seleccionan
    if fecha_inicio and fecha_fin:
        postulados_activos = postulados_activos.filter(Fecha_postulacion__date__range=[fecha_inicio, fecha_fin])

    # Obtener todas las carreras para el filtro
    carreras = Carreras.objects.all()

    return render(request, 'listarBecados.html', {
        'postulados': postulados_activos,
        'carrera_seleccionada': carrera_seleccionada,
        'carreras': carreras,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

@login_required  
def descargarBecados(request):
    # Filtrar postulados que están activos
    postulados_activos = postulado.objects.filter(esactivo__isnull=False)

    # Crear la respuesta HTTP
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="postulados_activos.csv"'

    # Crear el objeto CSV writer
    writer = csv.writer(response)
    writer.writerow(['Nombre', 'Apellido', 'Cédula', 'Fecha de Nacimiento', 'Grupo Étnico', 'Teléfono', 'Dirección', 'Correo', 'Fecha de Postulación', 'Estatus'])  # Encabezados

    for p in postulados_activos:
        # Escribir cada fila en el CSV
        writer.writerow([
            p.Nombres,
            p.Apellidos,
            p.Cedula_P,
            p.Fechanacimiento.strftime('%Y-%m-%d'),
            p.GrupoEtnico,
            p.N_TLF,
            p.Direccion,
            p.CorreoE,
            p.Fecha_postulacion.strftime('%Y-%m-%d'),
            p.estatus
        ])

    return response
