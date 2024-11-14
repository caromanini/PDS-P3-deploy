# lockers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Locker
from .forms import LockerPasswordForm, LockerEmailForm
from email.mime.image import MIMEImage
import os
import paho.mqtt.client as mqtt

# Configuracion MQTT
# broker = '192.168.54.124'
broker = 'locker_project.koyeb.app'
# broker = '172.31.162.160'
# broker = '186.10.216.200'
port = 1883
topic_send = "esp32/message"
topic_response = "django/response"
client_id = "django-client"
client = mqtt.Client(client_id)

def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código de resultado: {rc}")
    client.subscribe(topic_send)
    client.subscribe(topic_response)

def on_message(client, userdata, msg):
    print(f"Mensaje recibido desde ESP32 en {msg.topic}: {msg.payload.decode()}")
    lockers = Locker.objects.all().order_by('id')

    if msg.topic == "django/response":
        locker = get_object_or_404(Locker, id=int(msg.payload.decode()))

        email_subject = 'Tu Locker se ha abierto!'
        email_body = f'Tu locker se ha abierto: Locker {locker.id}\n'
        
        email = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,  # Correo de envío
            [locker.owner_email]       # Correo del propietario
        )

        email.send(fail_silently=False)

client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port)
client.loop_start()

def index_view(request):
    lockers = Locker.objects.all().order_by('id')
    
    return render(request, 'lockers/index.html', {'lockers': lockers})

def change_password(request, locker_id):
    locker = get_object_or_404(Locker, id=locker_id)

    if request.method == 'POST':
        form = LockerPasswordForm(request.POST, instance=locker)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            form.save()

            # Mandar mensaje MQTT
            mqtt_message = f'{{"locker_id": {locker_id}, "message": "{new_password}"}}'
            client.publish(topic_send, mqtt_message)
            
            email_subject = 'Nueva contraseña para tu Locker'
            email_body = f'La nueva contraseña de tu locker es: {new_password}\n\nSímbolos de la contraseña:'
            
            email = EmailMessage(
                email_subject,
                email_body,
                settings.EMAIL_HOST_USER,  # Correo de envío
                [locker.owner_email]       # Correo del propietario
            )
            
            for digit in new_password:
                image_path = os.path.join(settings.BASE_DIR, f'lockers/static/lockers/images/{digit}.png')
                with open(image_path, 'rb') as img_file:
                    mime_image = MIMEImage(img_file.read())
                    mime_image.add_header('Content-ID', f'<{digit}>')
                    mime_image.add_header('Content-Disposition', 'inline', filename=f'{digit}.png')
                    email.attach(mime_image)

            email.send(fail_silently=False)
            
            return redirect('index')
    else:
        form = LockerPasswordForm(instance=locker)

    return render(request, 'lockers/change_password.html', {'form': form, 'locker': locker})

def change_owner_email(request, locker_id):
    locker = get_object_or_404(Locker, id=locker_id)

    if request.method == 'POST':
        form = LockerEmailForm(request.POST, instance=locker)
        if form.is_valid():
            new_email = form.cleaned_data['owner_email']
            form.save()
            return redirect('index')
    else:
        form = LockerEmailForm(instance=locker)

    return render(request, 'lockers/change_owner_email.html', {'form': form, 'locker': locker})