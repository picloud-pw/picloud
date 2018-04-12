from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render
from django.template.loader import render_to_string

from cloud.forms import UserInfoForm, UserStatus
from cloud.models import UserInfo
from cloud.tokens import account_activation_token
from cloud.views.recaptcha import recaptcha_is_valid
from cloud.views.user import validate_name, validate_course


def sign_up(request):
    error = ""
    user_info_form = UserInfoForm()
    if request.method == "POST":
        first_name = request.POST['first-name']
        if not validate_name(first_name, "default"):
            first_name = None
        last_name = request.POST['last-name']
        if not validate_name("default", last_name):
            last_name = None
        course = request.POST['course']
        if not validate_course(course):
            course = None
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        second_password = request.POST['second_password']
        user_info_form = UserInfoForm(request.POST, request.FILES)

        error = validate_signup(username, email, password, second_password)
        if error == "":
            if not (User.objects.filter(username__iexact=username).exists() or
                    User.objects.filter(email__iexact=email).exists()):
                if user_info_form.is_valid() and recaptcha_is_valid(request):

                    # заполнение основной информации
                    user = User.objects.create_user(username, email, password)
                    if first_name is not None:
                        user.first_name = first_name
                    if last_name is not None:
                        user.second_name = last_name
                    user.is_active = False
                    user.save()
                    # дополнительная информация
                    user_info = user_info_form.save(commit=False)
                    user_info.user = user
                    user_info.course = course
                    user_info.status = UserStatus.objects.get(title="Рядовой студент")
                    user_info.save()

                    # подтверждение почты (активация аккаунта)
                    send_acc_activate_letter(request, user, email)

                    msg = 'Пожалуйста, подтвердите адрес электронной почты для завершения регистрации.'
                    return render(request, 'message.html', {'message': msg})
                else:
                    error = "Форма заполнена неправильно."
                    return render(request, 'auth/signup.html', {'error': error, 'user_info_form': user_info_form})
            else:
                error = "Пользователь с таким логином уже существует!"
                return render(request, 'auth/signup.html', {'error': error, 'user_info_form': user_info_form})
        else:
            return render(request, 'auth/signup.html', {'error': error, 'user_info_form': user_info_form})
    else:
        return render(request, 'auth/signup.html', {'error': error, 'user_info_form': user_info_form})


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
    email = EmailMessage(mail_subject, msg, to=[email])
    email.send()
