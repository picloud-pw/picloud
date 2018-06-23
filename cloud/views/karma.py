from cloud.models import UserInfo, Post

REGISTRATION_BONUS = 20
POST_TEXT_BONUS = 5
POST_IMAGE_BONUS = 4
POST_LINK_BONUS = 3
POST_FILE_BONUS = 3

AVATAR_BONUS = 50
COURSE_BONUS = 30
PROGRAM_BONUS = 50
VK_BONUS = 100


def update_carma(user):
    karma = REGISTRATION_BONUS

    posts = Post.objects.filter(author=user).filter(is_approved=True)
    for post in posts:
        if post.text != "":
            karma += POST_TEXT_BONUS
        if post.link:
            karma += POST_LINK_BONUS
        if post.file:
            karma += POST_FILE_BONUS
        if post.image:
            karma += POST_IMAGE_BONUS

    user_info = UserInfo.objects.get(user=user)
    if user_info.program:
        karma += PROGRAM_BONUS
    if user_info.course is not None:
        karma += COURSE_BONUS
    if user_info.vk_id:
        karma += VK_BONUS
    # TODO вынести в отдельные константы
    if user_info.avatar != 'resources/default/user_ava.png':
        karma += AVATAR_BONUS

    user_info.karma = karma
    user_info.save()
