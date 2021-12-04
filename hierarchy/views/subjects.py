from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

from hierarchy.models import Subject, Department


def search_subjects(request):
    query = request.GET.get('q')
    department_id = request.GET.get('department_id')
    is_approved = request.GET.get('is_approved') in ['True', None]

    subjects = Subject.objects.all()

    if query is not None:
        subjects = subjects.filter(name__icontains=query)
    if department_id is not None:
        try:
            department = Department.objects.get(id=department_id)
            subjects = subjects.filter(departments=department)
        except ObjectDoesNotExist:
            return JsonResponse({
                'error': f'Department with id={department_id} does not exist'
            })
    if is_approved or (not is_approved and request.user.is_superuser):
        subjects = subjects.filter(is_approved=is_approved)

    return JsonResponse({'subjects': [
        s.as_dict() for s in subjects.order_by('semester')
    ]})


def get_subject(request):
    subject_id = request.GET.get('id')
    subject = Subject.objects.get(id=subject_id)
    return JsonResponse({'subject': subject.as_dict()})
