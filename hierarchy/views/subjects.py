from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.utils import timezone

from decorators import auth_required
from hierarchy.models import Subject, Department
from posts.models import Post
from students.models import StudentInfo


def search_subjects(request):
    query = request.GET.get('q')
    department_id = request.GET.get('department_id')
    is_approved = request.GET.get('is_approved') in ['True', None]
    author_id = request.GET.get('author_id')
    page = request.GET.get('page', 1)
    page_size = request.GET.get('page_size', 24)

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
    if author_id is not None:
        student_info = StudentInfo.objects.get(id=author_id)
        subject_ids = Post.objects.filter(
            author_id=student_info.user.pk,
            is_draft=False,
            is_approved=True
        ).values('subject__id')
        subjects = subjects.filter(id__in=subject_ids)
    if is_approved or (not is_approved and request.user.is_superuser):
        subjects = subjects.filter(is_approved=is_approved)

    subjects = subjects.order_by('semester')

    paginator = Paginator(subjects, page_size)
    try:
        subjects_page = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        subjects_page = paginator.page(page)
    except EmptyPage:
        subjects_page = paginator.page(paginator.num_pages)

    return JsonResponse({
        'subjects': [
            subject.as_dict() for subject in subjects_page
        ],
        'total_subjects': paginator.count,
        'page': int(page),
        'page_size': page_size,
        'total_pages': paginator.num_pages,
    })


def get_subjects_list(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)
    subjects = Subject.objects.filter(Q(author=request.user) | Q(is_approved=True))
    return JsonResponse({'subjects': [{
        'id': subject.id,
        'author_id': subject.author.id if subject.author is not None else None,
        'name': subject.name,
    } for subject in subjects]})


def get_subject(request):
    subject_id = request.GET.get('id')
    subject = Subject.objects.get(id=subject_id)
    return JsonResponse({'subject': subject.as_dict()})


@auth_required
def create_subject(request):
    title = request.POST.get('title')
    if title is None or len(title) < 3:
        return JsonResponse(status=400, data={'error': 'Title is not set or length less than 3.'})
    new_subject = Subject.objects.create(author=request.user, name=title, created_at=timezone.now())
    return JsonResponse({'subject': new_subject.as_dict()})


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
