#Con estas librerias de django podemos pintar vistas es decir codigo html y con redirect podemos redirecionar al dar click en un boton por ejemplo
from django.shortcuts import render, redirect

#Acac importamos todos los modelos del archivo modelo.py para poder realizar operaciones de Crud (crear, eliminar, actualizar,leer)
from .models import ZonaComun,Propietario, Persona,Residente,Inmueble,Apartamento,Parqueadero,CuartoUtil,Visitante,ZonaComunReserva,PQRSD,ComentarioPQRSD,Vehiculo,EncargadoZonaComun

#con estas librerias enviamos mensajes para ser usados en la paginas muy comun para mostrar por ejemplo registros exitosos.
from django.contrib import messages
from django.http import JsonResponse

# Vista para la página de inicio
def index(request):
    return render(request, 'index.html')

# Vista para la página de creación de zonas comunes
def zonascomunes(request):
    zonas_comunes = []
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        requiere_pago = request.POST.get('requiere_pago', 'off')
        monto = request.POST.get('monto', 0)
        requiere_deposito = request.POST.get('requiere_deposito', 'off')
        monto_deposito = request.POST.get('monto_deposito', 0)
        bloques_reserva = request.POST.get('bloques_reserva', 1)
        cancelacion_horas_previas = request.POST.get('cancelacion_horas_previas', 2)
        cantidad_personas_permitidas = request.POST.get('cantidad_personas_permitidas', 1)
        mismo_usuario_puede_reservar_consecutivamente = request.POST.get('mismo_usuario_puede_reservar_consecutivamente', 1)
        disponibilidad_semana = request.POST.get('disponibilidad_semana')
        disponibilidad_fin_de_semana = request.POST.get('disponibilidad_fin_de_semana')
        horario_inicio_semana = request.POST.get('horario_inicio_semana')
        horario_fin_semana = request.POST.get('horario_fin_semana')
        horario_inicio_finde = request.POST.get('horario_inicio_finde')
        horario_fin_finde = request.POST.get('horario_fin_finde')
        
        if requiere_pago == 'on':
            requiere_pago = True
        else:
            requiere_pago = False

        if requiere_deposito == 'on':
            requiere_deposito = True
        else:
            requiere_deposito = False

        # Crea una nueva instancia de ZonaComun
        zona_comun = ZonaComun(
            nombre=nombre,
            requiere_pago=requiere_pago,
            monto=monto,
            requiere_deposito=requiere_deposito,
            monto_deposito=monto_deposito,
            bloques_reserva=bloques_reserva,
            cancelacion_horas_previas=cancelacion_horas_previas,
            cantidad_personas_permitidas=cantidad_personas_permitidas,
            mismo_usuario_puede_reservar_consecutivamente=mismo_usuario_puede_reservar_consecutivamente,
            disponibilidad_semana=disponibilidad_semana,
            disponibilidad_fin_de_semana=disponibilidad_fin_de_semana,
            horario_inicio_semana=horario_inicio_semana,
            horario_fin_semana=horario_fin_semana,
            horario_inicio_finde=horario_inicio_finde,
            horario_fin_finde=horario_fin_finde,
        )
        # Guarda la instancia en la base de datos
        zona_comun.save()

        # Establece el mensaje de éxito
        messages.success(request, 'Zona Comun registrada exitosamente')

    zonas_comunes = ZonaComun.objects.all()
    zona_choices = ZonaComun.ZONA_CHOICES
    return render(request, 'zonascomunes.html', {'zona_choices': zona_choices,'zonas_comunes': zonas_comunes})

#vista para registrar residentes o propietarios aca se tiene en cuenta los datos de Personas
def registroresidentes(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        tipo_persona = request.POST.get('tipo_persona')
        tipo_identificacion = request.POST.get('tipo_identificacion')
        nombres = request.POST.get('nombres')
        apellidos = request.POST.get('apellidos')
        razon_social = request.POST.get('razon_social')
        numero_contacto = request.POST.get('numero_contacto')
        correo_electronico = request.POST.get('correo_electronico')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        departamento = request.POST.get('departamento')
        rol = request.POST.get('rol') 
        numero_identificacion =request.POST.get('numero_identificacion')
        edad=request.POST.get('edad')

        # Crea una instancia de Persona
        persona = Persona.objects.create(
            tipo_persona=tipo_persona,
            tipo_identificacion=tipo_identificacion,
            nombres=nombres,
            apellidos=apellidos,
            razon_social=razon_social,
            numero_contacto=numero_contacto,
            correo_electronico=correo_electronico,
            direccion=direccion,
            ciudad=ciudad,
            departamento=departamento,
            numero_identificacion=numero_identificacion,
            edad=edad
        )

        # Según el valor de "rol", crea una instancia de Propietario o Residente
        if rol == 'Propietario':
            propietario = Propietario.objects.create(persona=persona)
        elif rol == 'Residente':
            residente = Residente.objects.create(persona=persona)

         # Establece el mensaje de éxito
        messages.success(request, 'Persona registrada exitosamente')
        return redirect('registroresidentes') 
    return render(request, 'registroresidentes.html')

#vista para rgistrar los inmuebles 
def registroinmuebles(request):
    # Obtén los propietarios y residentes
    propietarios = Propietario.objects.all()
    residentes = Residente.objects.all()

    if request.method == 'POST':
        # Obtén los datos del formulario que fueron enviados
        nomenclatura = request.POST.get('nomenclatura')
        coeficiente = request.POST.get('coeficiente')
        tipo_inmueble = request.POST.get('tipo_inmueble')

        inmueble = Inmueble(nomenclatura=nomenclatura, coeficiente=coeficiente)
        inmueble.save()

        if tipo_inmueble == 'Apartamento':
            numero_apartamento = request.POST.get('numero_apartamento')
            torre = request.POST.get('torre')
            residentes_ids = request.POST.getlist('residentes')

            apartamento = Apartamento(inmueble=inmueble, numero_apartamento=numero_apartamento, torre=torre)
            apartamento.save()
            apartamento.residentes.set(residentes_ids)
            residentes_autorizados_ids = request.POST.getlist('residentes_autorizados')
            apartamento.residentes_autorizados.set(residentes_autorizados_ids)  # Asigna los residentes autorizados
        elif tipo_inmueble == 'Parqueadero':
            parqueadero = Parqueadero(inmueble=inmueble)
            parqueadero.save()
        elif tipo_inmueble == 'CuartoUtil':
            cuarto_util = CuartoUtil(inmueble=inmueble)
            cuarto_util.save()

        # Asigna los propietarios al inmueble en general
        propietarios_ids = request.POST.getlist('propietarios')
        inmueble.propietarios.set(propietarios_ids)

        messages.success(request, 'Inmueble registrada exitosamente')
        return redirect('registroinmuebles')  

    return render(request, 'registroinmuebles.html', {'propietarios': propietarios, 'residentes': residentes})

#vista para registrar visitantes
def registrovisitantes(request):
    if request.method == 'POST':
        fecha_hora_ingreso = request.POST.get('fecha_hora_ingreso')
        tipo_identificacion = request.POST.get('tipo_identificacion')
        numero_identificacion = request.POST.get('numero_identificacion')
        nombres_completos = request.POST.get('nombres_completos')
        numero_contacto = request.POST.get('numero_contacto')
        unidad_residencial_id = request.POST.get('unidad_residencial')
        vehiculo = request.POST.get('vehiculo') == 'on'
        placa_vehiculo = request.POST.get('placa_vehiculo')
        parqueadero_visitante = request.POST.get('parqueadero_visitante')

        if not parqueadero_visitante:
            parqueadero_visitante = None
        else:
            try:
                parqueadero_visitante = int(parqueadero_visitante)
            except ValueError:
                return render(request, 'registrovisitantes.html', {'error': 'El campo "Número de Parqueadero Asignado" debe ser un número válido'})

        # Validar otros campos requeridos
        if not (fecha_hora_ingreso and tipo_identificacion and numero_identificacion and nombres_completos and numero_contacto and unidad_residencial_id):
            return render(request, 'registrovisitantes.html', {'error': 'Todos los campos son requeridos'})

        unidad_residencial = Apartamento.objects.get(id=unidad_residencial_id)

        visitante = Visitante(
            fecha_hora_ingreso=fecha_hora_ingreso,
            tipo_identificacion=tipo_identificacion,
            numero_identificacion=numero_identificacion,
            nombres_completos=nombres_completos,
            numero_contacto=numero_contacto,
            unidad_residencial=unidad_residencial,
            vehiculo=vehiculo,
            placa_vehiculo=placa_vehiculo,
            parqueadero_visitante=parqueadero_visitante
        )

        visitante.save()
        # Establece el mensaje de éxito
        messages.success(request, 'Visitante registrado con exito')

        return redirect('registrovisitantes')
    else:
        return render(request, 'registrovisitantes.html', {'apartamentos': Apartamento.objects.all()})

#vista para obtener los residentes que ya han sido autorizados
def obtener_residentes_autorizados(request, apartamento_id):
    try:
        # Obtén el apartamento con el ID proporcionado 
        apartamento = Apartamento.objects.get(id=apartamento_id)

        # Obtén los residentes autorizados para ese apartamento
        residentes_autorizados = apartamento.residentes_autorizados.all()

        # Convierte los datos en un diccionario
        data = {
            'residentes_autorizados': [
                {
                    'nombres': residente.persona.nombres,
                    'numero_contacto': residente.persona.numero_contacto,
                }
                for residente in residentes_autorizados
            ]
        }

        # Devuelve los datos en formato JSON
        return JsonResponse(data)
    except Apartamento.DoesNotExist:
        # Manejar el caso en el que el apartamento no existe
        data = {
            'residentes_autorizados': []
        }
        return JsonResponse(data)

#vista para almacenar las reservas
def reservas(request):
    if request.method == 'POST':
        zona_comun_nombre = request.POST.get('zonaComun')
        numero_apartamento_id = request.POST.get('numero_apartamento')
        visitantes = request.POST.getlist('visitantes')
        dias_reserva = request.POST['dias_reserva']
        horarios_disponibles = request.POST.get("horarios_disponibles")
        horarios_disponibles2 = request.POST.get("horarios_disponibles2")
        recibo_pago = request.POST.get("reciboPago", "false") == "true"
        deposito_entregado = request.POST.get("depositoEntregado", "false") == "true"


        if not horarios_disponibles:
            # Si "horarios_disponibles" no está presente, usa "horarios_disponibles"
            horarios_disponibles = horarios_disponibles2
        # Buscar la instancia de ZonaComun por su nombre
        zona_comun = ZonaComun.objects.get(nombre=zona_comun_nombre)

        # Buscar la instancia de Apartamento por su ID
        numero_apartamento = Apartamento.objects.get(id=numero_apartamento_id)
        # Crea una nueva instancia de ZonaComunReserva
        reserva = ZonaComunReserva(
            zona_comun=zona_comun,
            numero_apartamento=numero_apartamento,
            hora_reserva=horarios_disponibles, 
            recibo_pago=recibo_pago,
            deposito_entregado=deposito_entregado,
            dias_reserva=dias_reserva
        )
        reserva.save()
        # Establece el mensaje de éxito
        messages.success(request, 'Reserva registrada exitosamente')

        # Agrega los visitantes a la reserva (puedes personalizar esto según tus necesidades)
        for visitante_id in visitantes:
            reserva.visitantes.add(visitante_id)

        # Realiza cualquier otra lógica necesaria

        return redirect('reservas')  
    
    zonas_comunes = ZonaComun.objects.all()
    visitantes = Visitante.objects.all()
    apartamento = Apartamento.objects.all()
    return render(request, 'reservas.html', {'zonas_comunes': zonas_comunes,'visitantes': visitantes, 'apartamentos':apartamento})

#vista para crear los pqr y almacenarlo en la bd
def pqrss(request):
    if request.method == 'POST':
        numero_apartamento = request.POST.get('numero_apartamento')
        tipo_pqrsd = request.POST.get('tipo_pqrsd')
        forma_respuesta = request.POST.get('forma_respuesta')
        respuesta_direccion = request.POST.get('respuesta_direccion', '')
        contenido = request.POST.get('contenido')
        # Captura de la fecha y hora de registro
        fecha_hora_registro = request.POST.get('fecha_hora_registro')

        forma_respuesta = request.POST.get('forma_respuesta')
        if forma_respuesta == "Escrita":
            respuesta_direccion = request.POST.get('respuesta_direccion')
            barrio = request.POST.get('barrio')
            municipio = request.POST.get('municipio')
            departamento = request.POST.get('departamento')
        else:
            respuesta_direccion = None
            barrio = None
            municipio = None
            departamento = None
        
        # Crear la PQRSD
        pqrsd = PQRSD.objects.create(
            numero_apartamento=numero_apartamento,
            tipo_pqrsd=tipo_pqrsd,
            contenido=contenido,
            fecha_hora_registro=fecha_hora_registro, 
            forma_respuesta=forma_respuesta,
            respuesta_direccion=respuesta_direccion,
            barrio=barrio,
            municipio=municipio,
            departamento=departamento,
        )
            
        estado = 'En proceso'  # Estado inicial
        responsable = 'Administrador'  # Responsable inicial

        pqrsd.estado = estado
        pqrsd.responsable = responsable
        pqrsd.save()
        # Establece el mensaje de éxito
        messages.success(request, 'PQRSD registrada exitosamente')
   
        return redirect('pqrs')  
    residentes = Residente.objects.all() 
    apartamentos = Apartamento.objects.all() 
    return render(request, 'pqrs.html',{'apartamentos': apartamentos,'residentes': residentes})

#vista para crear los registros de vehiculos ocn su responsble
def registrovehiculos(request):
    if request.method == 'POST':
        marca = request.POST.get('marca')
        modelo = request.POST.get('modelo')
        placa = request.POST.get('placa')
        responsable_id = request.POST.get('responsable')

        # Guardar el vehículo en la base de datos
        vehiculo = Vehiculo.objects.create(marca=marca, modelo=modelo, placa=placa)

         # Asignar el vehículo al residente seleccionado
        if responsable_id:
            responsable = Residente.objects.get(id=responsable_id)
            vehiculo.responsable = responsable
            vehiculo.save()
            # Establece el mensaje de éxito
            messages.success(request, 'Vehiculo registrado exitosamente')

        return redirect('registrovehiculos')  # Redirige a la lista de vehículos registrados

    residentes = Residente.objects.all() 
    return render(request, 'registrovehiculos.html', {'residentes': residentes})

#vsita para regstrar a los encargados de cada zona
def registroencargados(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo_electronico = request.POST.get('correo_electronico')
        numero_contacto = request.POST.get('numero_contacto')
        zona_comun_id = request.POST.get('zona_comun_asignada')

        try:
            zona_comun = ZonaComun.objects.get(pk=zona_comun_id)
            encargado = EncargadoZonaComun.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo_electronico=correo_electronico,
                numero_contacto=numero_contacto,
                zona_comun_asignada=zona_comun
            )
            # Establece el mensaje de éxito
            messages.success(request, 'Encargado de Zona Comun registrado exitosamente')
            return redirect('registroencargados')
        except ZonaComun.DoesNotExist:
            pass

    zonas_comunes = ZonaComun.objects.all()
    return render(request, 'registroencargados.html', {'zonas_comunes': zonas_comunes})

# vista para mostrar los datos de ls pqrsd
def procesarpqrs(request):
    pqrs_list = PQRSD.objects.all()
    return render(request, 'procesarpqrs.html', {'pqrs_list': pqrs_list})

#vista para procesar editar el estado y crear los comentarios
def procesar_pqr(request, pqr_id):
    if request.method == 'POST':
        pqr = PQRSD.objects.get(pk=pqr_id)
        pqr.estado = request.POST.get('estado')
        pqr.responsable = request.POST.get('responsable')
        pqr.save()
        # Establece el mensaje de éxito
        messages.success(request, 'Gestión de PQRSD guardada exitosamente')

        comentario = request.POST.get('comentario')
        if comentario:
            ComentarioPQRSD.objects.create(pqrsd=pqr, nombre_responsable=pqr.responsable, comentario=comentario)

        return redirect('procesarpqrs')

    return redirect('procesarpqrs')

#vista para obtener los detalles de la pqrsd a comentar 
def obtener_detalle_pqr(request, pqr_id):
    try:
        pqr = PQRSD.objects.get(pk=pqr_id)
        pqr_details = {
            'numero_apartamento': pqr.numero_apartamento,
            'tipo_pqrsd': pqr.tipo_pqrsd,
            'contenido': pqr.contenido,
            'estado': pqr.estado,
            'responsable': pqr.responsable,
            # Agrega otros detalles que desees
        }
        return JsonResponse(pqr_details)
    except PQRSD.DoesNotExist:
        return JsonResponse({'error': 'PQRSD no encontrada'})
    
#vista para mostrar el informe de las zonas reservadas
def listadoreservas(request):
    reservas = ZonaComunReserva.objects.select_related('zona_comun', 'numero_apartamento').all()
    return render(request, 'listadoreservas.html', {'reservas': reservas})

#vista para almacenar la información de las lista de pqr y su proceso
def listadopqrs(request):
    pqrs = PQRSD.objects.all()
    return render(request, 'listadopqrs.html', {'pqrs': pqrs})

#vsita para mostrar los inmuebles con sus propietarios y residentes
def listadoinmuebles(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'listadoinmuebles.html', {'inmuebles': inmuebles})