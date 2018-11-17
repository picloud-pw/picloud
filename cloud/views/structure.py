from django.http import JsonResponse
from django.views.decorators.cache import cache_page

from cloud.models import University, Department, Chair


@cache_page(60 * 15)
def hierarchy_dump(request):
    return JsonResponse({
        'universities': {u.id: u.as_hierarchical_dict() for u in University.objects.filter(is_approved=True)},
    })
