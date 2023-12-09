from django.db import models
#Creación de modelos para las migraciones a la base de datos 

#Tabla zona comun  aca se almacena toda información de las zonas comunes que hay en el conjunto
class ZonaComun(models.Model):
    ZONA_CHOICES = (
        ('SalonSocial', 'Salón Social'),
        ('ZonaBBQ', 'Zona BBQ'),
        ('CanchaSintetica', 'Cancha Sintética'),
        ('ZonaHumeda', 'Zona Húmeda'),
        # Agrega más zonas a medida que se habiliten
    )

    nombre= models.CharField(max_length=20, choices=ZONA_CHOICES)
    requiere_pago = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)
    requiere_deposito = models.BooleanField(default=False)
    monto_deposito = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,default=0)
    bloques_reserva = models.PositiveIntegerField(default=1)
    cancelacion_horas_previas = models.PositiveIntegerField(default=2)
    cantidad_personas_permitidas = models.PositiveIntegerField(default=1)
    mismo_usuario_puede_reservar_consecutivamente = models.PositiveIntegerField(default=1)
    disponibilidad_semana = models.CharField(max_length=100)
    disponibilidad_fin_de_semana = models.CharField(max_length=100)
    horario_inicio_semana = models.TimeField()
    horario_fin_semana = models.TimeField()
    horario_inicio_finde = models.TimeField()
    horario_fin_finde = models.TimeField()

#Tabla Personas crea todos los datos que podria tener una persona en el conjunto recidencial
class Persona(models.Model):
    TIPO_PERSONA_CHOICES = (
        ('Natural', 'Persona Natural'),
        ('Juridica', 'Persona Jurídica'),
    )
    TIPO_IDENTIFICACION_CHOICES = (
        ('TI', 'Tarjeta de Identidad'),
        ('CC', 'Cédula de Ciudadanía'),
        ('NIT', 'Número de Identificación Tributaria'),
    )

    tipo_persona = models.CharField(max_length=10, choices=TIPO_PERSONA_CHOICES)
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_IDENTIFICACION_CHOICES)
    numero_identificacion = models.CharField(max_length=20) 
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    numero_contacto = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    direccion = models.CharField(max_length=150)
    ciudad = models.CharField(max_length=50)
    departamento = models.CharField(max_length=50)
    edad = models.PositiveIntegerField()

#Tabla propietario esta tabla se relacona con una persona 
class Propietario(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

#Tabla Residente esta tabla se relaciona con la tabla persona y esta relacionada uno a uno con OneToOneField que se garantiza que no puede haber duplicados en la relación, tambien se relacioan el vehiulo que tiene el residente s es que lo tiene
class Residente(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True, related_name='vehiculos_responsable')

#Tabla Vehiculo esta tabla tiene todos los atributos de un vehiculo y su residente asociado a el vehiculo
class Vehiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10)
    responsable = models.ForeignKey(Residente, on_delete=models.CASCADE, related_name='vehiculos_responsable', null=True, blank=True)

#Tabla inmueble esta tabla tiene todos los atributos que tiene un inmueble y su propietario
class Inmueble(models.Model):
    nomenclatura = models.CharField(max_length=50)
    coeficiente = models.DecimalField(max_digits=5, decimal_places=2)
    propietarios = models.ManyToManyField(Propietario)

#Esta tabla tiene relación con un inmueble que sera de tipo Parquedero
class Parqueadero(models.Model):
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE)

#Esta tabla tiene relación con un inmueble que sera de tipo cuartoutil
class CuartoUtil(models.Model):
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE)

#Esta tabla tiene relación con un inmueble que sera de tipo Apartamento asu vez ete apratamento tene relacion con los residente los cuales pueden ser muchos ManyToManyField por eso se usa una relación de muchos a muhos
class Apartamento(models.Model):
    inmueble = models.OneToOneField(Inmueble, on_delete=models.CASCADE)
    numero_apartamento = models.CharField(max_length=10)
    torre = models.CharField(max_length=20)
    residentes = models.ManyToManyField(Residente, related_name='apartamentos')
    residentes_autorizados = models.ManyToManyField(Residente, related_name='apartamentos_autorizados')

#La tabla visitante tiene toda la información de un visitante incluido si tiene vehiculo y el parquedero
class Visitante(models.Model):
    TIPO_IDENTIFICACION_CHOICES = (
        ('Ti', 'TI'),
        ('CC', 'CC'),
        ('CT', 'CT'),
    )
    fecha_hora_ingreso = models.DateTimeField()
    tipo_identificacion = models.CharField(max_length=2, choices=TIPO_IDENTIFICACION_CHOICES)
    numero_identificacion = models.CharField(max_length=20, blank=True, null=True)
    nombres_completos = models.CharField(max_length=100)
    numero_contacto = models.CharField(max_length=20)
    unidad_residencial = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='visitantes')
    vehiculo = models.BooleanField(default=False)
    placa_vehiculo = models.CharField(max_length=20, blank=True, null=True)
    parqueadero_visitante = models.PositiveIntegerField(blank=True, null=True)

#Tabla de reservas esta toma los datos de las zona comun y almacena la información de una reserva realizada por un residente
class ZonaComunReserva(models.Model):
    zona_comun = models.ForeignKey(ZonaComun, on_delete=models.CASCADE)
    numero_apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE)
    hora_reserva = models.CharField(max_length=100)
    recibo_pago = models.BooleanField(default=False)
    deposito_entregado = models.BooleanField(default=False)
    visitantes = models.ManyToManyField(Visitante)
    dias_reserva = models.CharField(max_length=100)

#esta tabla acrea los campos necesarios para almacenar los datos de las pqrsd asi como su estado y el nombre de un responsable d eresponderla
class PQRSD(models.Model):
    TIPO_RESPUESTA_CHOICES = (
        ('Correo electrónico', 'Correo electrónico'),
        ('Escrita', 'Escrita'),
    )
    ESTADO_CHOICES = (
        ('En proceso', 'En proceso'),
        ('Finalizado', 'Finalizado'),
    )
    
    numero_apartamento = models.CharField(max_length=10)
    fecha_hora_registro = models.DateTimeField(auto_now_add=True)
    tipo_pqrsd = models.CharField(max_length=100)
    forma_respuesta = models.CharField(max_length=20, choices=TIPO_RESPUESTA_CHOICES)
    respuesta_direccion = models.CharField(max_length=150, blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    contenido = models.TextField() 
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='En proceso')
    responsable = models.CharField(max_length=100)

#Tabla comentarios esta almacena los comentarios que realize un responssable acerca de la pqrsd asi como tambien indica si ya finalizo o no el estado de la pqrsd
class ComentarioPQRSD(models.Model):
    pqrsd = models.ForeignKey(PQRSD, on_delete=models.CASCADE)
    fecha_hora = models.DateTimeField(auto_now_add=True)
    nombre_responsable = models.CharField(max_length=100)
    comentario = models.TextField()

#modelo encargados
class EncargadoZonaComun(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    numero_contacto = models.CharField(max_length=20)
    zona_comun_asignada = models.ForeignKey('ZonaComun', on_delete=models.CASCADE)



