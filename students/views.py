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
        user_info.user.username = username

    if first_name is not None:
        user_info.user.first_name = first_name

    if last_name is not None:
        user_info.user.last_name = last_name

    if department_id is not None:
        department = Department.objects.get(id=department_id)
        user_info.department = department

    user_info.user.save()
    user_info.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Changes saved',
    })


@auth_required
def search(request):
    page = request.GET.get('p', 1)
    page_size = request.GET.get('ps', 15)

    students = StudentInfo.objects.all()

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
