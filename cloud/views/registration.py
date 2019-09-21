from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render
from django.template.loader import render_to_string

from cloud.forms import UserStatus
from cloud.models import UserInfo
from cloud.tokens import account_activation_token
from cloud.views.recaptcha import recaptcha_is_valid


@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        user_info = UserInfo(user=instance)
        user_info.status = UserStatus.objects.get(title="Рядовой студент")
        user_info.save()


def sign_up(request):
    error = ""
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        second_password = request.POST['second_password']

        error = validate_signup(username, email, password, second_password)
        if error == "":
            if not (User.objects.filter(username__iexact=username).exists() or
                    User.objects.filter(email__iexact=email).exists()):
                if recaptcha_is_valid(request):
                    user = User.objects.create_user(username, email, password)
                    user.is_active = False
                    user.save()

                    if send_acc_activate_letter(request, user, email):
                        msg = 'Пожалуйста, подтвердите адрес электронной почты для завершения регистрации.'
                        return render(request, 'message.html', {'message': msg})
                    else:
                        error = "Ошибка при отправке сообщения для подтверждения почты."
                        return render(request, 'auth/signup.html', {'error': error})
                else:
                    error = "ReCaptcha не пройдена, попробуйте снова."
                    return render(request, 'auth/signup.html', {'error': error})
            else:
                error = "Пользователь с таким логином или почтой уже существует!"
                return render(request, 'auth/signup.html', {'error': error})
        else:
            return render(request, 'auth/signup.html', {'error': error})
    else:
        return render(request, 'auth/signup.html', {'error': error})


def validate_signup(username, email, password, second_password):
    error = ""
    if len(username) > 15 or len(username) < 3:
        error = "Некорректно задан логин. (Длина должна быть от 3 до 15 символов)"
    if len(password) < 5:
        error = "Некорректно задан пароль. (Длина должна быть не менее 5 символов)"
    if email is None or email == "" or len(email) > 128:
        error = "Некорректно задана почта"
    if password != second_password:
        error = "Пароли не совпадают"
    return error


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        request.session['user_avatar_url'] = UserInfo.objects.get(user=user).avatar.url
        program = UserInfo.objects.get(user=user).program
        if program is not None:
            request.session['program_id'] = program.pk
        else:
            request.session['program_id'] = ""

        msg = 'Почта подтверждена! Теперь вы можете заходить в свой личный кабинет!'
        return render(request, 'message.html', {'message': msg})
    else:
        msg = 'Ссылка недействительна. Обратитесь в службу обратной связи, если возникла проблема.'
        return render(request, 'message.html', {'message': msg})


def send_acc_activate_letter(request, user, email):
    current_site = get_current_site(request)
    mail_subject = 'Активация аккаунта PiCloud'
    msg = render_to_string('auth/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': user.pk,
        'token': account_activation_token.make_token(user),
    })
    try:
        email = EmailMessage(mail_subject, msg, to=[email])
        email.send()
    except Exception:
        return False
    else:
        return True
