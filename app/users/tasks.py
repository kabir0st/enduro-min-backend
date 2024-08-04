from core.celery import celery_app
from core.tasks import write_log_file
from django.apps import apps
from django.core.mail import send_mail
from django.template.loader import render_to_string


@celery_app.task
def send_otp_email(pk):
    try:
        model = apps.get_model('users.VerificationCode')
        obj = model.objects.get(id=pk)
        template = 'VerifyEmail'
        title = 'Action Required: Verify Your HTR Account.'
        if obj.otp_for == 'password_reset':
            template = 'PasswordReset'
            title = 'Reset Your HTR Account\'s Password.'
        if msg_html := render_to_string(f"emails/{template}.html",
                                        {'otp': obj.code}):
            if _ := send_mail(subject=title,
                              message="",
                              from_email="HTR <lurayy36@gmail.com>",
                              recipient_list=[obj.email],
                              html_message=msg_html,
                              fail_silently=False):
                obj.is_email_sent = True
                obj.save()
    except Exception as exp:
        print(exp)
        write_log_file('otp', f'{obj.email} : {exp}', True)
