from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from decorators import auth_required
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


@auth_required
def approve_subject(request):
    subject_id = request.POST.get('id')
    if subject_id is None:
        return HttpResponse(status=404)
    subject = Subject.objects.get(id=subject_id)
    if request.user.is_authenticated and \
            (request.user.is_staff or request.user.is_superuser):
        subject.is_approved = True
        subject.save()
    return HttpResponse(status=200)


@auth_required
def delete_subject(request):
    subject_id = request.POST.get('id')
    if subject_id is None:
        return HttpResponse(status=404)
    subject = Subject.objects.get(id=subject_id)
    if request.user.is_authenticated and request.user.is_superuser:
        subject.delete()
    return HttpResponse(status=200)
