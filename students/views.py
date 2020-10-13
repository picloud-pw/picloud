from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse

from decorators import auth_required
from .models import StudentInfo


@auth_required
def me(request):
    user_info = StudentInfo.objects.get(user=request.user)
    return JsonResponse(user_info.as_dict())


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
