from cloud.models import UserInfo, Post, Department
from django.shortcuts import get_object_or_404, render, redirect

REGISTRATION_BONUS = 20
POST_TEXT_BONUS = 5
POST_IMAGE_BONUS = 4
POST_LINK_BONUS = 3
POST_FILE_BONUS = 3

AVATAR_BONUS = 50
COURSE_BONUS = 30
PROGRAM_BONUS = 50
VK_BONUS = 100

DEFAULT_AVATAR_URL = 'resources/default/user_ava.png'


def update_carma(user):
    karma = REGISTRATION_BONUS

    posts = Post.objects.filter(author=user).filter(is_approved=True)
    for post in posts:
        if post.text != "":
            karma += POST_TEXT_BONUS
        if post.link:
            karma += POST_LINK_BONUS
        if post.file:
            karma += POST_FILE_BONUS
        if post.image:
            karma += POST_IMAGE_BONUS

    user_info = UserInfo.objects.get(user=user)
    if user_info.program:
        karma += PROGRAM_BONUS
    if user_info.course is not None:
        karma += COURSE_BONUS
    if user_info.vk_id:
        karma += VK_BONUS
    # TODO вынести в отдельные константы
    if user_info.avatar != DEFAULT_AVATAR_URL:
        karma += AVATAR_BONUS

    user_info.karma = karma
    user_info.save()


def info_page(request, user_id):
    if request.user.is_authenticated:
        update_carma(request.user)

        posts = Post.objects.filter(author=request.user).filter(is_approved=True)
        user_info = UserInfo.objects.get(user=request.user)

        rb = REGISTRATION_BONUS
        ptb = POST_TEXT_BONUS
        pib = POST_IMAGE_BONUS
        plb = POST_LINK_BONUS
        pfb = POST_FILE_BONUS
        ab = AVATAR_BONUS
        cb = COURSE_BONUS
        pb = PROGRAM_BONUS
        vkb = VK_BONUS
        dau = DEFAULT_AVATAR_URL

        global_top = None
        users = UserInfo.objects.all().order_by("karma").reverse()
        for index, user in enumerate(users):
            if user.user == request.user:
                global_top = index

        univer_top = None
        departs = Department.objects.filter(university=user_info.program.chair.department.university)
        users = users.filter(program__chair__department__in=departs)
        for index, user in enumerate(users):
            if user.user == request.user:
                univer_top = index

        depart_top = None
        users = users.filter(program__chair__department=user_info.program.chair.department)
        for index, user in enumerate(users):
            if user.user == request.user:
                depart_top = index

        return render(request, 'karma.html', locals())
    else:
        return redirect("cloud")
