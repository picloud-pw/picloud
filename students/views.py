from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse

from decorators import auth_required
from hierarchy.models import Department
from .models import StudentInfo, StudentStatus


@auth_required
def me(request):
    user_info = StudentInfo.objects.get(user=request.user)
    return JsonResponse(user_info.as_dict())


@auth_required
def me_edit(request):
    user_info = StudentInfo.objects.get(user=request.user)

    avatar = request.POST.get('avatar')
    username = request.POST.get('username')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    department_id = request.POST.get('department_id')

    if username is not None:
        if User.objects.filter(username=username).count():
            return JsonResponse({
                'status': 'warning',
                'message': 'This username is already taken',
            })
        if 16 < len(username) or len(username) < 4:
            return JsonResponse({
                'status': 'warning',
                'message': 'Length must be between 4 and 16 characters.',
            })
        user_info.user.username = username

    if first_name is not None:
        if 30 < len(first_name):
            return JsonResponse({
                'status': 'warning',
                'message': 'Length must be up to 30 characters.',
            })
        user_info.user.first_name = first_name

    if last_name is not None:
        if 30 < len(last_name):
            return JsonResponse({
                'status': 'warning',
                'message': 'Length must be up to 30 characters.',
            })
        user_info.user.last_name = last_name

    if department_id is not None:
        try:
            department = Department.objects.get(id=department_id)
        except ObjectDoesNotExist:
            return JsonResponse({
                'status': 'warning',
                'message': 'Department_id is incorrect.',
            })
        user_info.department = department

    user_info.user.save()
    user_info.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Changes saved',
    })


@auth_required
def get(request):
    student_id = request.GET.get('id')

    student = StudentInfo.objects.get(id=student_id)

    return JsonResponse(student.as_dict())


@auth_required
def search(request):
    query = request.GET.get('q')
    department_id = request.GET.get('department_id')
    is_avatar_set = request.GET.get('avatar')
    status_id = request.GET.get('status_id')
    page = request.GET.get('p', 1)
    page_size = request.GET.get('ps', 15)

    students = StudentInfo.objects.all()

    if query is not None:
        students = students.filter(user__username__icontains=query)

    if department_id is not None:
        students = students.filter(department_id=department_id)

    if status_id is not None:
        students = students.filter(status_id=status_id)

    if is_avatar_set is not None:
        def_ava = Q(avatar=StudentInfo.avatar.field.default)
        students = students.filter(~def_ava if is_avatar_set else def_ava)

    paginator = Paginator(students, page_size)
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = list()

    return JsonResponse({'students': [
        student.as_dict() for student in students_page
    ]})


@auth_required
def get_statuses(request):
    statuses = StudentStatus.objects.all()
    return JsonResponse({'statuses': [
        status.as_dict() for status in statuses
    ]})
