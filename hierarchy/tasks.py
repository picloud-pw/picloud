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
                name=faculty['title'],
                is_approved=True,
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
                    name=chair['title'],
                    is_approved=True,
                )


migrate_rules = {
    'ВТ': '1102',
    'ИПМ': '1762',
    'ГТ': '1771',
    'КОТ': '1776739',
    'ФиК': '1611',
    'ИС': '1750',
    'ИТГС': '1780',
    'КТ': '1748',
    'ИТТЭК': '1871415',
    'ПБКС': '1758',
    'ИКС': '1937284',
    'СУиИ': '9412',
    'нет': '1713080',
}


def migrate_hierarchy():
    p_level, created = DepartmentType.objects.get_or_create(name='Program')
    for chair in Chair.objects.all():
        try:
            rule = migrate_rules[chair.short_title]
            c_department = Department.objects.get(
                department_type__name='Chair',
                short_name=rule
            )
        except Exception as e:
            print(e)
            continue
        for program in Program.objects.filter(chair=chair):
            p_department, created = Department.objects.get_or_create(
                department_type=p_level,
                parent_department=c_department,
                name=program.title,
                short_name=program.code,
                link=program.link,
                is_approved=program.is_approved,
            )
            for subject in Subject.objects.filter(programs=program):
                new_subject, created = NewSubject.objects.get_or_create(
                    name=subject.title,
                    short_name=subject.short_title,
                    semester=subject.semester,
                    is_approved=subject.is_approved,
                )
                new_subject.departments.add(p_department)

                for post in Post.objects.filter(subject=subject):
                    _migrate_post(post, new_subject)


def _migrate_post(post: Post, subject: NewSubject):
    if post.parent_post is not None:
        parent_post = _migrate_post(post.parent_post, subject)
    else:
        parent_post = None
    new_post_type, created = NewPostType.objects.get_or_create(
        title=post.type.title,
        plural=post.type.plural,
    )
    new_post, created = NewPost.objects.get_or_create(
        subject=subject,
        type=new_post_type,
        author=post.author,
        parent_post=parent_post,
        last_editor=post.last_editor,
        title=post.title,
        text=post.text,
        created_date=post.created_date,
        image=post.image,
        link=post.link,
        views=post.views,
        file=post.file,
        is_approved=post.is_approved,
    )
    for comment in Comment.objects.filter(post=post):
        new_comment, created = NewComment.objects.get_or_create(
            author=comment.author,
            post=new_post,
            text=comment.text,
            created_date=comment.created_date,
        )
    return new_post
