import vk
from django.conf import settings

from cloud.models import Chair, Program, Subject, Post, Comment
from hierarchy.models import DepartmentType, Department, Subject as NewSubject
from posts.models import Post as NewPost, PostType as NewPostType, Comment as NewComment

GLOBAL_TOKEN = getattr(settings, 'VK_GLOBAL_TOKEN', None)
API_VERSION = '5.103'


def update_hierarchy():
    session = vk.Session(access_token=GLOBAL_TOKEN)
    vk_api = vk.API(session)
    u_level, created = DepartmentType.objects.get_or_create(name='University')
    f_level, created = DepartmentType.objects.get_or_create(name='Faculty')
    c_level, created = DepartmentType.objects.get_or_create(name='Chair')
    for university in Department.objects.filter(department_type=u_level):
        faculties = vk_api.database.getFaculties(
            university_id=university.short_name,
            count=10000,
            v=API_VERSION,
        )
        for faculty in faculties['items']:
            faculty_in_db, created = Department.objects.get_or_create(
                department_type=f_level,
                parent_department=university,
                short_name=faculty['id'],
                name=faculty['title']
            )
            chairs = vk_api.database.getChairs(
                faculty_id=faculty['id'],
                count=10000,
                v=API_VERSION,
            )
            for chair in chairs['items']:
                chair_in_db, created = Department.objects.get_or_create(
                    department_type=c_level,
                    parent_department=faculty_in_db,
                    short_name=chair['id'],
                    name=chair['title']
                )
