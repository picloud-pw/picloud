from django.core.exceptions import ObjectDoesNotExist
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.http import JsonResponse, HttpResponse

from decorators import auth_required
from hierarchy.models import Department, DepartmentType


def get_department_types(request):
    return JsonResponse([
        d.as_dict() for d in DepartmentType.objects.all()
    ], safe=False)


def get_department(request):
    department_id = request.GET.get('id')

    department = Department.objects.get(id=department_id)

    return JsonResponse({
        'department': department.as_dict(),
        'hierarchy': department.get_hierarchy(),
        'statistics': {},
    })


def search_departments(request):
    query = request.GET.get('q')
    department_type_id = request.GET.get('department_type_id')
    parent_department_id = request.GET.get('parent_department_id')
    is_approved = request.GET.get('is_approved') in ['True', None]

    departments = Department.objects.all()

    if query is not None:
        departments = departments.filter(name__icontains=query)
    if department_type_id is not None:
        try:
            department_type = DepartmentType.objects.get(id=department_type_id)
            departments = departments.filter(department_type=department_type)
        except ObjectDoesNotExist:
            return JsonResponse({
                'error': f'DepartmentType with id={department_type_id} does not exist'
            })
    if parent_department_id is not None:
        try:
            if parent_department_id != 'null':
                department = Department.objects.get(id=parent_department_id)
            else:
                department = None
            departments = departments.filter(parent_department=department)
        except ObjectDoesNotExist:
            return JsonResponse({
                'error': f'Department with id={parent_department_id} does not exist'
            })
    if is_approved or (not is_approved and request.user.is_superuser):
        departments = departments.filter(is_approved=is_approved)

    departments = departments.annotate(
        vk_id_int=Cast('vk_id', IntegerField())
    ).order_by('vk_id_int')

    return JsonResponse({
        'departments': [d.as_dict() for d in departments]
    })


@auth_required
def approve_department(request):
    department_id = request.POST.get('id')
    if department_id is None:
        return HttpResponse(status=404)
    department = Department.objects.get(id=department_id)
    if request.user.is_authenticated and \
            (request.user.is_staff or request.user.is_superuser):
        department.is_approved = True
        department.save()
    return HttpResponse(status=200)


@auth_required
def delete_department(request):
    department_id = request.POST.get('id')
    if department_id is None:
        return HttpResponse(status=404)
    department = Department.objects.get(id=department_id)
    if request.user.is_authenticated and request.user.is_superuser:
        department.delete()
    return HttpResponse(status=200)
