import vk
from django.http import JsonResponse, HttpResponse

from hierarchy.models import DepartmentType, Department
from PiCloud.settings.common import VK_GLOBAL_TOKEN, VK_API_VERSION


def search_universities(request):
    session = vk.Session(access_token=VK_GLOBAL_TOKEN)
    vk_api = vk.API(session)

    universities = vk_api.database.getUniversities(
        q=request.GET.get('q', ''),
        city_id=request.GET.get('city_id'),
        count=10,
        v=VK_API_VERSION,
    )

    return JsonResponse({'universities': universities['items']})


def add_university(request):
    full_university_name = request.POST.get('full_university_name')
    u_id = request.POST.get('university_id')
    u_city_id = request.POST.get('city_id')

    exist_university = Department.objects.filter(vk_id=u_id, department_type__name='University')
    if exist_university.count():
        return JsonResponse(exist_university.first().as_dict())

    session = vk.Session(access_token=VK_GLOBAL_TOKEN)
    vk_api = vk.API(session)
    university = [u for u in vk_api.database.getUniversities(
        q=full_university_name,
        city_id=u_city_id,
        count=10,
        v=VK_API_VERSION,
    )['items'] if str(u['id']) == u_id][0]

    u_level, created = DepartmentType.objects.get_or_create(name='University')
    university_obj, created = Department.objects.get_or_create(
        vk_id=university['id'],
        department_type=u_level,
        defaults={
            'name': university['title'],
            'vk_city_id': u_city_id,
            'is_approved': True,
        }
    )
    update_university_hierarchy(university_obj)
    return JsonResponse(university_obj.as_dict())


def update_university_hierarchy(university: Department):
    session = vk.Session(access_token=VK_GLOBAL_TOKEN)
    vk_api = vk.API(session)
    if university.department_type.name != 'University':
        raise ValueError('Incorrect department type')

    f_level, created = DepartmentType.objects.get_or_create(name='Faculty')
    c_level, created = DepartmentType.objects.get_or_create(name='Chair')

    faculties = vk_api.database.getFaculties(
        university_id=university.vk_id,
        count=10000,
        v=VK_API_VERSION,
    )
    for faculty in faculties['items']:
        faculty_in_db, created = Department.objects.get_or_create(
            department_type=f_level,
            parent_department=university,
            vk_id=faculty['id'],
            defaults={
                'name': faculty['title'],
                'is_approved': True,
            }
        )
        chairs = vk_api.database.getChairs(
            faculty_id=faculty['id'],
            count=10000,
            v=VK_API_VERSION,
        )
        for chair in chairs['items']:
            chair_in_db, created = Department.objects.get_or_create(
                department_type=c_level,
                parent_department=faculty_in_db,
                vk_id=chair['id'],
                defaults={
                    'name': chair['title'],
                    'is_approved': True,
                }
            )
