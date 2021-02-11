from hierarchy.models import DepartmentType, Department
from hierarchy.tasks import update_hierarchy, migrate_hierarchy
from memes.tasks import migrate_memes
from students.tasks import migrate_user_infos


def create_start_universities():
    u_level, created = DepartmentType.objects.get_or_create(name='University')
    Department.objects.create(
        department_type=u_level,
        name="Университет ИТМО",
        short_name="53",
        is_approved=True,
    )
    Department.objects.create(
        department_type=u_level,
        name="МГУ им. Н.П.Огарева",
        short_name="792",
        is_approved=True,
    )
    Department.objects.create(
        department_type=u_level,
        name="ГУУ",
        short_name="131",
        is_approved=True,
    )


def migrate():
    create_start_universities()
    update_hierarchy()
    migrate_hierarchy()

    migrate_memes()

    migrate_user_infos()





