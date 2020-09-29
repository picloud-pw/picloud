from cloud.views.vkontakte import vk_bot

VALID = 0
NOT_VALID = 1

# Starting VK bot
# FIXME: This MUST NOT be here!
# t = threading.Thread(target=vk_bot)
# t.daemon = True
# t.start()

from . import (
    api,
    authentication,
    chairs,
    departments,
    memes,
    message,
    posts,
    programs,
    recaptcha,
    registration,
    search,
    subjects,
    structure,
    universities,
    user,
    karma,
    vkontakte,
)
