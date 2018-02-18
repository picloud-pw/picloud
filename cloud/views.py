import threading
import time
import feedparser
import json

from dateutil import parser
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.template.loader import render_to_string
from django.contrib.staticfiles.templatetags.staticfiles import static

from .forms import *
from .tokens import account_activation_token


def robots(request):
    return render_to_response('robots.txt', content_type="text/plain")


def post_list(request):
    posts = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date').reverse()
    return render(request, 'cloud/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.views < 99999:
        post.views += 1
        post.save()
    return render(request, 'cloud/post_detail.html', {'post': post})


def post_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            request.session['last_post_subject'] = request.POST["subject"]
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.created_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
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
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                post.save()
                return redirect('post_detail', pk=post.pk)
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


def message(request, msg):
    return render(request, 'message.html', {message: msg})


def signout(request):
    auth.logout(request)
    return redirect("post_list")


def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            request.session['user_ava_url'] = UserInfo.objects.get(user=user).avatar.url
            return redirect('post_list')
        else:
            error = "Не верно введены логин или пароль!"
            return render(request, 'auth/signin.html', {'error': error})
    else:
        error = ""
        return render(request, 'auth/signin.html', {'error': error})


def validate_signup(username, email, password, second_password):
    error = ""
    if len(username) > 10 or len(username) < 5:
        error = "Некорректно задан логин"
    if len(password) < 5:
        error = "Некорректно задан пароль"
    if email is None or email == "" or len(email) > 128:
        error = "Некорректно задана почта"
    if password != second_password:
        error = "Пароли не совпадают"
    return error


def send_acc_activate_letter(request, user, email):
    current_site = get_current_site(request)
    mail_subject = 'Активация PiCloud аккаунта'
    msg = render_to_string('auth/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': user.pk,
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(mail_subject, msg, to=[email])
    email.send()


def signup(request):
    error = ""
    user_info_form = UserInfoForm()
    if request.method == "POST":
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        second_password = request.POST['second_password']
        user_info_form = UserInfoForm(request.POST, request.FILES)

        error = validate_signup(username, email, password, second_password)
        if error == "":
            if not (User.objects.filter(username__iexact=username).exists() or
                    User.objects.filter(email__iexact=email).exists()):
                if user_info_form.is_valid():

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
                    user_info.status = UserStatus.objects.get(title="Рядовой студент")
                    user_info.save()

                    # подтверждение почты (активация аккаунта)
                    send_acc_activate_letter(request, user, email)

                    msg = 'Пожалуйста подтвердите адрес элетронной почты для завершения регистрации'
                    return render(request, 'message.html', {'message': msg})
                else:
                    error = "Не все поля формы прошли валидацию!"
                    return render(request, 'auth/signup.html', {'error': error, 'user_info_form': user_info_form})
            else:
                error = "Такой пользователь уже существует!"
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
        msg = 'Почта подтверждена! Теперь вы можете заходить в свой личный кабинет!'
        return render(request, 'message.html', {'message': msg})
    else:
        msg = 'Ссылка не корректна! Обратитесь в службу обратной связи с этой проблемой!'
        return render(request, 'message.html', {'message': msg})


def search(request):
    university = ChooseUniversityForm()
    department = ChooseDepartmentForm()
    chair = ChooseChairForm()
    program = ChooseProgramForm()
    subject = ChooseSubjectForm()
    return render(request, 'search.html', {'university': university,
                                           'department': department,
                                           'chair': chair,
                                           'program': program,
                                           'subject': subject,
                                           })


def memes_update(sleep_interval):
    while True:
        feeds_rss = []
        feed_col_1 = []
        feed_col_2 = []
        counter = 0
        vk_urls_rss = [
            "http://feed.exileed.com/vk/feed/klimenkovdefacto/?owner=1&only_admin=1",
            "http://feed.exileed.com/vk/feed/pashasmeme/?owner=1&only_admin=1",
            "http://feed.exileed.com/vk/feed/dnische1/?owner=1&only_admin=1",
            "http://feed.exileed.com/vk/feed/itmoquotepad/?owner=1&only_admin=1",
            "http://feed.exileed.com/vk/feed/wisemrduck/?owner=1&only_admin=1",
        ]
        for url in vk_urls_rss:
            feeds = feedparser.parse(url)["entries"]
            feeds_rss.extend(feeds)
        if len(feeds_rss) > 0:
            for feed in feeds_rss:
                feed["published"] = parser.parse(feed.published).strftime("%y.%m.%d %H:%M")
            feeds_rss.sort(key=lambda x: x['published'], reverse=True)
            for feed in feeds_rss:
                if counter % 2 == 0:
                    feed_col_1.append(feed)
                else:
                    feed_col_2.append(feed)
                counter += 1
            global feeds_mem
            feeds_mem = [feed_col_1, feed_col_2]
            with open('memes.txt', 'w') as outfile:
                json.dump(feeds_mem, outfile)
            print("Memes updated! -- " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            time.sleep(sleep_interval)
        else:
            feeds_mem = json.load(open(static('memes.txt')))
            print("Error updating memes! Try again in an hour! --" + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
            time.sleep(60*60)


feeds_mem = []
t = threading.Thread(target=memes_update, args=(60*60*12,))
t.daemon = True
t.start()


def memes(request):
    return render(request, 'memes.html', {'colomns_feed': feeds_mem})


def settings(request, message=""):
    change_avatar_form = AvatarChangeForm()
    change_password_form = PasswordChangeForm(request.user)
    user = User.objects.get(pk=request.user.pk)
    user_info = UserInfo.objects.get(user=user)
    return render(request, 'settings.html', {'user': user,
                                             'user_info': user_info,
                                             'change_password_form': change_password_form,
                                             'change_avatar_form': change_avatar_form,
                                             'message': message,
                                             }
                  )


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

    return render(request, "structure/university_page.html", {"univer": univer,
                                                              "departments": departments,
                                                              "chairs": chairs,
                                                              "programs": programs,
                                                              "stats": {"posts": posts,
                                                                        "views": views,
                                                                        "persons": persons
                                                                        }
                                                              }
                  )


def program_page(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    subjects = Subject.objects.filter(programs=program)
    semesters = set()
    for sub in subjects:
        semesters.add(sub.semestr)
    return render(request, "structure/program_page.html", {"program": program,
                                                           "subjects": subjects,
                                                           "semesters": semesters,
                                                           }
                  )


def subject_page(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    posts = Post.objects.filter(subject=subject)
    post_types = set()
    for post in posts:
        post_types.add(post.type)
    return render(request, "structure/subject_page.html", {"subject": subject,
                                                           "posts": posts,
                                                           "post_types": post_types,
                                                           }
                  )


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
            msg = "Ваш email отправлен! Спасибо за обращение! Оно будет рассмотрено в ближайшее время!"
            return render(request, 'message.html', {'message': msg})
        else:
            msg = "Ваше сообщение не было отправленно! Не все поля заполнены корректно!"
            return render(request, 'message.html', {'message': msg})
    else:
        form = ContactForm()
        return render(request, 'contacts.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            return settings(request, message='Пароль успешно изменен!')
        else:
            return settings(request, message='Пароли введены с ошибкой!')
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings(request, message='Пароль должен быть длиннее 8 символов!')


def change_avatar(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST,
                                request.FILES,
                                instance=UserInfo.objects.get(user=request.user))
        if form.is_valid():
            form.save()
            request.session['user_ava_url'] = UserInfo.objects.get(user=request.user).avatar.url
            return settings(request)
        else:
            return settings(request)
    else:
        # не достижимый участок кода, только если на прямую обратиться по адресу
        return settings(request)


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
    posts = Post.objects.all()
    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)
    posts = posts.order_by('created_date').reverse()
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)


def search_posts(request):
    words = request.GET.get('search_request', None).split(" ")
    posts = Post.objects.all()
    posts = posts.order_by('created_date').reverse()
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)
