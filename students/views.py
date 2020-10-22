from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from decorators import auth_required
from hierarchy.models import Department
from .models import StudentInfo


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
        user_info.user.username = username

    if first_name is not None:
        if 30 < first_name:
            return JsonResponse({
                'status': 'warning',
                'message': 'Length must be up to 30 characters.',
            })
        user_info.user.first_name = first_name

    if last_name is not None:
        if 30 < last_name:
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
def search(request):
    query = request.GET.get('q')
    page = request.GET.get('p', 1)
    page_size = request.GET.get('ps', 15)

    students = StudentInfo.objects.all()

    if query is not None:
        students = students.filter(user__username__icontains=query)

    paginator = Paginator(students, page_size)
    try:
        students_page = paginator.page(page)
    except PageNotAnInteger:
        students_page = paginator.page(1)
    except EmptyPage:
        students_page = paginator.page(paginator.num_pages)

    return JsonResponse({'students': [
        student.as_dict() for student in students_page
    ]})
