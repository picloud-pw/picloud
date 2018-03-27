import json
import urllib
import threading

from .vkontakte import *

from django.conf import settings
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string

from .forms import *
from .tokens import account_activation_token

# constants
POSTS_PER_PAGE = 12


# vk bot start
t = threading.Thread(target=vk_bot)
t.daemon = True
t.start()


def index(request):
    if request.user.is_authenticated:
        return redirect("post_list")
    else:
        return render(request, 'index.html', {})


def robots(request):
    return render_to_response('robots.txt', content_type="text/plain")


def post_list(request, display_posts=None):
    e_m = ""
    if request.user.is_authenticated:
        user_info = UserInfo.objects.get(user=request.user)
        if user_info.program is not None:
            user_program_id = user_info.program.pk
            posts = Post.objects.filter(validate_status=0) \
                .filter(created_date__lte=timezone.now()) \
                .filter(subject__programs__exact=user_program_id) \
                .order_by('created_date').reverse()
        else:
            posts = Post.objects.filter(validate_status=0) \
                .filter(created_date__lte=timezone.now()) \
                .order_by('created_date').reverse()
        if display_posts is not None:
            posts = display_posts
            e_m = "Данный пользователь пока не поделился своими материалами."
    else:
        posts = Post.objects.filter(validate_status=0) \
            .filter(created_date__lte=timezone.now()) \
            .order_by('created_date').reverse()

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'cloud/post_list.html', {'posts': posts_page, 'empty_message': e_m})


def validation(request):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):

        posts = Post.objects.filter(validate_status=1).order_by('created_date')

        page = request.GET.get('page', 1)
        paginator = Paginator(posts, POSTS_PER_PAGE)
        try:
            posts_page = paginator.page(page)
        except PageNotAnInteger:
            posts_page = paginator.page(1)
        except EmptyPage:
            posts_page = paginator.page(paginator.num_pages)
        return render(request, 'validation.html', {'posts': posts_page})

    else:
        return redirect("post_list")


def post_detail(request, pk, msg=""):
    post = get_object_or_404(Post, pk=pk)
    if post.views < 99999:
        post.views += 1
        post.save()
    return render(request, 'cloud/post_detail.html', {'post': post, 'message': msg})


def get_validate_status(user):
    user_status = UserInfo.objects.get(user=user).status
    if user_status.status_level > 7 or user.is_superuser or user.is_staff:
        return 0
    else:
        return 1


def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
            v_s = get_validate_status(request.user)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.created_date = timezone.now()
                post.validate_status = v_s
                post.save()
                request.session['last_post_subject'] = request.POST["subject"]
                if v_s == 0:
                    return redirect('post_detail', pk=post.pk)
                else:
                    msg = "Спасибо за ваш вклад! Мы уже уведомлены о вашем посте, он будет проверен в ближайшее время."
                    return post_detail(request, pk=post.pk, msg=msg)
            else:
                form = PostForm()
                user_info = get_object_or_404(UserInfo, user=request.user)
                return render(request, 'cloud/post_edit.html', {'form': form, 'user_info': user_info})
        else:
            form = PostForm()
            user_info = get_object_or_404(UserInfo, user=request.user)
            return render(request, 'cloud/post_edit.html', {'form': form, 'user_info': user_info})
    else:
        return redirect("post_list")


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (request.user.is_authenticated and request.user.is_staff) or request.user.pk == post.author.pk:
        if request.method == "POST":
            form = PostForm(request.POST, request.FILES, instance=post)
            v_s = get_validate_status(request.user)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.validate_status = v_s
                post.save()
                if v_s == 0:
                    return redirect('post_detail', pk=post.pk)
                else:
                    msg = "Благодарим за правки! В ближайшее время мы проверим и опубликуем их."
                    return post_detail(request, pk=post.pk, msg=msg)
            else:
                form = PostForm(instance=post)
                user_info = get_object_or_404(UserInfo, user=request.user)
                return render(request, 'cloud/post_edit.html', {'form': form, 'post': post})
        else:
            form = PostForm(instance=post)
            user_info = get_object_or_404(UserInfo, user=request.user)
            return render(request, 'cloud/post_edit.html', {'form': form, 'post': post})
    else:
        return redirect("post_list")


def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if (request.user.is_authenticated and request.user.is_staff) or request.user.pk == post.author.pk:
        post.delete()
        return redirect("post_list")
    else:
        return redirect("post_list")


def post_checked(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Post.objects.filter(pk=pk).update(validate_status=0)
        return redirect("validation")
    else:
        return redirect("post_list")


def message(request, msg):
    return render(request, 'message.html', {'message': msg})


def signout(request):
    auth.logout(request)
    return redirect("index")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)

            request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
            program = UserInfo.objects.get(user=user).program
            if program is not None:
                request.session['program_id'] = program.pk
            else:
                request.session['program_id'] = ""

            return redirect('post_list')
        else:
            error = "Неверно введены логин или пароль!"
            return render(request, 'auth/signin.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/signin.html', {'error': error})


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


def validate_course(course):
    try:
        c = int(course)
        return 0 <= c <= 10
    except ValueError:
        return False


def validate_name(first_name, last_name):
    return len(first_name) < 20 and len(last_name) < 20


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


def recaptcha_is_valid(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    url = 'https://www.google.com/recaptcha/api/siteverify'
    values = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    data = urllib.parse.urlencode(values).encode()
    req = urllib.request.Request(url, data=data)
    response = urllib.request.urlopen(req)
    result = json.loads(response.read().decode())

    return result['success']


def signup(request):
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

                    msg = 'Пожалуйста, подтвердите адрес элетронной почты для завершения регистрации.'
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


def activate(request, uid, token):
    try:
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
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


def search(request):
    university = ChooseUniversityForm()
    department = ChooseDepartmentForm()
    chair = ChooseChairForm()
    program = ChooseProgramForm()
    subject = ChooseSubjectForm()
    user_info = UserInfo.objects.filter(user=request.user.pk).first()
    return render(request, 'search.html', {
        'university': university,
        'department': department,
        'chair': chair,
        'program': program,
        'subject': subject,
        'user_info': user_info,
    })


def universities_list(request):
    univer_list = University.objects.all()
    return render(request, 'structure/universities.html', {"univer_list": univer_list})


def university_page(request, university_id):
    univer = get_object_or_404(University, pk=university_id)
    departments = Department.objects.filter(university_id=university_id)
    chairs = Chair.objects.filter(department__university__id=university_id)
    programs = Program.objects.filter(chair__department__university_id=university_id)

    posts_queryset = Post.objects.filter(subject__programs__in=programs).distinct()
    posts = posts_queryset.count()
    views = 0
    for post in posts_queryset:
        views += post.views
    persons = UserInfo.objects.filter(program__in=programs).count()

    return render(request, "structure/university_page.html", {
        "univer": univer,
        "departments": departments,
        "chairs": chairs,
        "programs": programs,
        "stats": {
            "posts": posts,
            "views": views,
            "persons": persons
        }
    })


def program_page(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    subjects = Subject.objects.filter(programs=program)
    semesters = set()
    for sub in subjects:
        semesters.add(sub.semestr)
    return render(request, "structure/program_page.html", {
        "program": program,
        "subjects": subjects,
        "semesters": semesters,
    })


def subject_page(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    posts = Post.objects.filter(subject=subject).filter(validate_status=0)
    post_types = set()
    for post in posts:
        post_types.add(post.type)
    return render(request, "structure/subject_page.html", {
        "subject": subject,
        "posts": posts,
        "post_types": post_types,
    })


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['contact_name']
            email = form.cleaned_data['contact_email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            mail_msg = content + " <<< " + email + " >>>" + "(((" + name + ")))"
            email = EmailMessage(subject, mail_msg, email, to=["itmo.cloud@gmail.com"])
            email.send()
            msg = "Спасибо! Письмо отправлено. Ваше обращение будет рассмотрено в ближайшее время."
            return render(request, 'message.html', {'message': msg})
        else:
            msg = "Форма заполнена неправильно. Письмо не было отправлено."
            return render(request, 'message.html', {'message': msg})
    else:
        form = ContactForm()
        return render(request, 'contacts.html', {'form': form})


def get_memes(request):
    memes = fetch_and_sort_memes_from_all_groups()
    return render(request, "memes.html", {"memes": memes})


def user_page(request, user_id):
    if request.user.is_authenticated:
        fr_user = get_object_or_404(User, pk=user_id)
        fr_user_info = UserInfo.objects.get(user=fr_user)
        return render(request, 'user.html', locals())
    else:
        return message(request, msg="Авторизуйтесь, чтобы посещать страницы других пользователей.")


def user_posts(request, user_id):
    if request.user.is_authenticated:
        fr_user = User.objects.get(pk=user_id)
        fr_user_posts = Post.objects \
            .filter(author=fr_user) \
            .filter(validate_status=0) \
            .filter(created_date__lte=timezone.now()) \
            .order_by('created_date') \
            .reverse()
        return post_list(request, display_posts=fr_user_posts)
    else:
        return message(request, msg="Авторизуйтесь, чтобы просматривать посты конкретных пользователей.")


def user_not_checked_posts(request, user_id):
    if request.user.is_authenticated and int(user_id) == request.user.pk:
        user = User.objects.get(pk=user_id)
        not_validate_posts = Post.objects \
            .filter(author=user) \
            .filter(validate_status=1) \
            .filter(created_date__lte=timezone.now()) \
            .order_by('created_date') \
            .reverse()
        return post_list(request, display_posts=not_validate_posts)
    else:
        return message(request, msg="Вы можете просматривать только проверенные посты этого пользователя.")


def settings_page(request, msg="", error=""):
    change_avatar_form = AvatarChangeForm()
    change_password_form = PasswordChangeForm(request.user)
    change_user_form = UserChangeForm(instance=User.objects.get(pk=request.user.pk))
    change_user_info_form = UserInfoChangeForm(instance=UserInfo.objects.get(user=request.user))
    user = User.objects.get(pk=request.user.pk)
    user_info = UserInfo.objects.get(user=user)
    return render(request, 'settings.html', {'user': user,
                                             'user_info': user_info,
                                             'change_password_form': change_password_form,
                                             'change_avatar_form': change_avatar_form,
                                             'change_user_form': change_user_form,
                                             'change_user_info_form': change_user_info_form,
                                             'message': msg,
                                             'error': error,
                                             }
                  )


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return settings_page(request, msg='Пароль успешно изменен.')
        else:
            return settings_page(request, error='Пароли введены с ошибкой.')
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings_page(request, error='Пароль должен быть длиннее 8 символов.')


def change_avatar(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST,
                                request.FILES,
                                instance=UserInfo.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            request.session['user_ava_url'] = UserInfo.objects.get(user=request.user).avatar.url
            return settings_page(request, msg="Аватар успешно изменен.")
        else:
            return settings_page(request, error="При изменении аватара произошла ошибка.")
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings_page(request)


def change_user(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=User.objects.get(pk=request.user.pk))
        user_info_form = UserInfoChangeForm(request.POST, instance=UserInfo.objects.get(user=request.user))
        if user_form.is_valid() and validate_name(request.POST['first_name'], request.POST['last_name']):
            user_form.save()
        else:
            return settings_page(request, error="Ошибка при изменении данных. " +
                                                "Убедитесь, что длина полей «Имя» и «Фамилия» не превышает 20 символов")
        if user_info_form.is_valid() and validate_course(request.POST['course']):
            user_info_form.save()

            program = UserInfo.objects.get(user=request.user).program
            if program is not None:
                request.session['program_id'] = program.pk
            else:
                request.session['program_id'] = ""
        else:
            return settings_page(request, error="Ошибка при изменении данных. " +
                                                "Убедитесь, что поля «Программа обучения» и «Курс обучения» заполнены")
        return settings_page(request, msg="Данные успешно сохранены.")
    else:
        # недостижимый участок кода, только если на прямую обратиться по адресу
        return settings_page(request)


def get_universities(request):
    dictionaries = [obj.as_dict() for obj in University.objects.all()]
    return JsonResponse(dictionaries, safe=False)


def get_departments(request):
    university_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Department.objects.filter(university=university_id)]
    return JsonResponse(dictionaries, safe=False)


def get_chairs(request):
    department_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Chair.objects.filter(department=department_id)]
    return JsonResponse(dictionaries, safe=False)


def get_programs(request):
    chair_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Program.objects.filter(chair=chair_id)]
    return JsonResponse(dictionaries, safe=False)


def get_subjects(request):
    program_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in Subject.objects.filter(programs=program_id).order_by('semestr')]
    return JsonResponse(dictionaries, safe=False)


def get_posts(request):
    program_id = request.GET.get('program_id', None)
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    posts = Post.objects.filter(validate_status=0)
    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_posts(request):
    words = request.GET.get('search_request', None).lover().split(" ")
    posts = Post.objects.filter(validate_status=0)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_and_render_posts(request):
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    posts = Post.objects.filter(validate_status=0)
    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)
    posts = posts.order_by('created_date').reverse()[:100]

    page = request.GET.get('page', 1)
    paginator = Paginator(posts, POSTS_PER_PAGE)
    try:
        posts_page = paginator.page(page)
    except PageNotAnInteger:
        posts_page = paginator.page(1)
    except EmptyPage:
        posts_page = paginator.page(paginator.num_pages)

    return render(request, 'cloud/bare_post_list.html', {'posts': posts_page})


def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')
