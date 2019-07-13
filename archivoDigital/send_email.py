from django.conf import settings
from django.core.mail import send_mail
from django.template import loader

def sender(tipo,to,subject,passW,area_documento_usuario):
    from_email=settings.EMAIL_HOST_USER
    to_email=[to]
    print(passW)
    #Bienvenida nuevo usuario
    if tipo==1:
        html_message = loader.render_to_string(
                    'email/email_bienvenida_adc.html',
                    {
                        'Usuario':  to,
                        'Contra':   passW,
                    }
                )
    #Notificacion de bloqueo a usuario
    elif tipo==2:
        Message = 'Clave de acceso:{}'.format(passW)
    #Notificacion de desbloqueo a usuario
    elif tipo==3:
        html_message = loader.render_to_string(
                    'email/email_bloqueousuario_adc.html',
                    {
                        'Motivo':  'Supero el numero de intentos para acceder a un area/documento definido como restringido(a)',
                    }
                )
    #Cambio de contraseña a usuario/area/documentos
    elif tipo==4:
        html_message = loader.render_to_string(
                    'email/email_actualizacioncontraseña_adc.html',
                    {
                        'tipo':  area_documento_usuario,
                        'Contra':  passW,
                    }
                )

    send_mail(subject=subject,from_email=from_email,recipient_list=to_email,fail_silently=True,html_message=html_message,message='')

def senderMany(to,subject,passW,area_documento_usuario):
    from_email=settings.EMAIL_HOST_USER
    to_email=to

    html_message = loader.render_to_string(
                'email/email_actualizacioncontraseña_adc.html',
                {
                    'tipo':  area_documento_usuario,
                    'Contra':  passW,
                }
            )
    send_mail(subject=subject,from_email=from_email,recipient_list=to_email,fail_silently=True,html_message=html_message,message='')
