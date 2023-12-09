# Generated by Django 4.2.6 on 2023-10-27 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Apartamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_apartamento', models.CharField(max_length=10)),
                ('torre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Inmueble',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nomenclatura', models.CharField(max_length=50)),
                ('coeficiente', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_persona', models.CharField(choices=[('Natural', 'Persona Natural'), ('Juridica', 'Persona Jurídica')], max_length=10)),
                ('tipo_identificacion', models.CharField(choices=[('TI', 'Tarjeta de Identidad'), ('CC', 'Cédula de Ciudadanía'), ('NIT', 'Número de Identificación Tributaria')], max_length=5)),
                ('numero_identificacion', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(blank=True, max_length=100, null=True)),
                ('razon_social', models.CharField(blank=True, max_length=100, null=True)),
                ('numero_contacto', models.CharField(max_length=20)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=150)),
                ('ciudad', models.CharField(max_length=50)),
                ('departamento', models.CharField(max_length=50)),
                ('edad', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='PQRSD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_apartamento', models.CharField(max_length=10)),
                ('fecha_hora_registro', models.DateTimeField(auto_now_add=True)),
                ('tipo_pqrsd', models.CharField(max_length=100)),
                ('forma_respuesta', models.CharField(choices=[('Correo electrónico', 'Correo electrónico'), ('Escrita', 'Escrita')], max_length=20)),
                ('respuesta_direccion', models.CharField(blank=True, max_length=150, null=True)),
                ('barrio', models.CharField(blank=True, max_length=100, null=True)),
                ('municipio', models.CharField(blank=True, max_length=100, null=True)),
                ('departamento', models.CharField(blank=True, max_length=100, null=True)),
                ('contenido', models.TextField()),
                ('estado', models.CharField(choices=[('En proceso', 'En proceso'), ('Finalizado', 'Finalizado')], default='En proceso', max_length=20)),
                ('responsable', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Residente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora_ingreso', models.DateTimeField()),
                ('tipo_identificacion', models.CharField(choices=[('Ti', 'TI'), ('CC', 'CC'), ('CT', 'CT')], max_length=2)),
                ('numero_identificacion', models.CharField(blank=True, max_length=20, null=True)),
                ('nombres_completos', models.CharField(max_length=100)),
                ('numero_contacto', models.CharField(max_length=20)),
                ('vehiculo', models.BooleanField(default=False)),
                ('placa_vehiculo', models.CharField(blank=True, max_length=20, null=True)),
                ('parqueadero_visitante', models.PositiveIntegerField(blank=True, null=True)),
                ('unidad_residencial', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visitantes', to='webapp.apartamento')),
            ],
        ),
        migrations.CreateModel(
            name='ZonaComun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('SalonSocial', 'Salón Social'), ('ZonaBBQ', 'Zona BBQ'), ('CanchaSintetica', 'Cancha Sintética'), ('ZonaHumeda', 'Zona Húmeda')], max_length=20)),
                ('requiere_pago', models.BooleanField(default=False)),
                ('monto', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('requiere_deposito', models.BooleanField(default=False)),
                ('monto_deposito', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True)),
                ('bloques_reserva', models.PositiveIntegerField(default=1)),
                ('cancelacion_horas_previas', models.PositiveIntegerField(default=2)),
                ('cantidad_personas_permitidas', models.PositiveIntegerField(default=1)),
                ('mismo_usuario_puede_reservar_consecutivamente', models.PositiveIntegerField(default=1)),
                ('disponibilidad_semana', models.CharField(max_length=100)),
                ('disponibilidad_fin_de_semana', models.CharField(max_length=100)),
                ('horario_inicio_semana', models.TimeField()),
                ('horario_fin_semana', models.TimeField()),
                ('horario_inicio_finde', models.TimeField()),
                ('horario_fin_finde', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ZonaComunReserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_reserva', models.CharField(max_length=100)),
                ('recibo_pago', models.BooleanField(default=False)),
                ('deposito_entregado', models.BooleanField(default=False)),
                ('dias_reserva', models.CharField(max_length=100)),
                ('numero_apartamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.apartamento')),
                ('visitantes', models.ManyToManyField(to='webapp.visitante')),
                ('zona_comun', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.zonacomun')),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=50)),
                ('modelo', models.CharField(max_length=50)),
                ('placa', models.CharField(max_length=10)),
                ('responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vehiculos_responsable', to='webapp.residente')),
            ],
        ),
        migrations.AddField(
            model_name='residente',
            name='vehiculo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehiculos_responsable', to='webapp.vehiculo'),
        ),
        migrations.CreateModel(
            name='Propietario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Parqueadero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inmueble', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.inmueble')),
            ],
        ),
        migrations.AddField(
            model_name='inmueble',
            name='propietarios',
            field=models.ManyToManyField(to='webapp.propietario'),
        ),
        migrations.CreateModel(
            name='EncargadoZonaComun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('numero_contacto', models.CharField(max_length=20)),
                ('zona_comun_asignada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.zonacomun')),
            ],
        ),
        migrations.CreateModel(
            name='CuartoUtil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inmueble', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.inmueble')),
            ],
        ),
        migrations.CreateModel(
            name='ComentarioPQRSD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField(auto_now_add=True)),
                ('nombre_responsable', models.CharField(max_length=100)),
                ('comentario', models.TextField()),
                ('pqrsd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.pqrsd')),
            ],
        ),
        migrations.AddField(
            model_name='apartamento',
            name='inmueble',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='webapp.inmueble'),
        ),
        migrations.AddField(
            model_name='apartamento',
            name='residentes',
            field=models.ManyToManyField(related_name='apartamentos', to='webapp.residente'),
        ),
        migrations.AddField(
            model_name='apartamento',
            name='residentes_autorizados',
            field=models.ManyToManyField(related_name='apartamentos_autorizados', to='webapp.residente'),
        ),
    ]