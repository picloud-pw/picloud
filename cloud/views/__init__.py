from cloud.views.vkontakte import vk_bot

VALID = 0
NOT_VALID = 1

# Starting VK bot
# FIXME: This MUST NOT be here!
# t = threading.Thread(target=vk_bot)
# t.daemon = True
# t.start()

from . import api, authentication, chairs, contacts, departments, index, legal, memes, message, moderation, posts, \
    programs, recaptcha, registration, robots, search, subjects, universities, user, karma, vkontakte
