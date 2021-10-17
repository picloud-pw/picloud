import vk
from django.http import JsonResponse

from PiCloud.settings.common import VK_API_VERSION, VK_GLOBAL_TOKEN


def search_cities(request):
    session = vk.Session(access_token=VK_GLOBAL_TOKEN)
    vk_api = vk.API(session)

    cities = vk_api.database.getCities(
        q=request.GET.get('q', ''),
        country_id='1',  # Russia
        count=10,
        v=VK_API_VERSION,
    )

    return JsonResponse({'cities': cities['items']})
