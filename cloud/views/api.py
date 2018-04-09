from django.http import JsonResponse

from cloud.models import University, Department, Chair, Program, Subject, Post
from . import VALID


def get_universities(request):
    dictionaries = [obj.as_dict() for obj in
                    University.objects.filter(validate_status=VALID)]
    return JsonResponse(dictionaries, safe=False)


def get_departments(request):
    university_id = request.GET.get('id', None)
    departments = [
        department.as_dict()
        for department
        in Department.objects
            .filter(university=university_id)
            .filter(validate_status=VALID)
    ]
    return JsonResponse(departments, safe=False)


def get_chairs(request):
    department_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in
                    Chair.objects.filter(department=department_id)
                        .filter(validate_status=VALID)]
    return JsonResponse(dictionaries, safe=False)


def get_programs(request):
    chair_id = request.GET.get('id', None)
    dictionaries = [obj.as_dict() for obj in
                    Program.objects.filter(chair=chair_id)
                        .filter(validate_status=VALID)]
    return JsonResponse(dictionaries, safe=False)


def get_subjects(request):
    program_id = request.GET.get('id', None)
    subjects = [
        subject.as_dict()
        for subject
        in Subject.objects \
            .filter(programs=program_id) \
            .order_by('semestr') \
            .filter(validate_status=VALID)
    ]
    return JsonResponse(subjects, safe=False)


def get_posts(request):
    program_id = request.GET.get('program_id', None)
    subject_id = request.GET.get('subject_id', None)
    type_id = request.GET.get('type_id', None)
    posts = Post.objects.filter(approved=True)
    if subject_id is not None:
        posts = posts.filter(subject=subject_id)
    if type_id is not None:
        posts = posts.filter(type=type_id)
    posts = posts.order_by('created_date').reverse()[:100]
    posts = [obj.as_dict() for obj in posts]
    return JsonResponse(posts, safe=False)
