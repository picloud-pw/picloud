from cloud.models import UserStatus, UserInfo

from website.models import UserStatus as NewUserStatus, UserInfo as NewUserInfo


def migrate_user_infos():
    for u_s in UserStatus.objects.all():
        NewUserStatus.objects.get_or_create(
            title=u_s.title,
            status_level=u_s.status_level,
            can_publish_without_moderation=u_s.can_publish_without_moderation,
            can_moderate=u_s.can_moderate,
        )

    for u_i in UserInfo.objects.all():
        new_status = NewUserStatus.objects.get(title=u_i.status.title)
        NewUserInfo.objects.get_or_create(
            avatar=u_i.avatar,
            user=u_i.user,
            status=new_status,
            karma=u_i.karma,
            course=u_i.course,
        )
