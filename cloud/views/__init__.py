from cloud.views.vkontakte import vk_bot

VALID = 0
NOT_VALID = 1

# Starting VK bot
# FIXME: This MUST NOT be here!
# t = threading.Thread(target=vk_bot)
# t.daemon = True
# t.start()

from . import api
from . import authentication
from . import chairs
from . import contacts
from . import departments
from . import index
from . import legal
from . import memes
from . import message
from . import moderation
from . import posts
from . import programs
from . import recaptcha
from . import registration
from . import robots
from . import search
from . import subjects
from . import structure
from . import universities
from . import user
from . import karma
from . import vkontakte
from . import comment