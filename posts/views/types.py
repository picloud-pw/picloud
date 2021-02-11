from django.http import JsonResponse

from posts.models import PostType


def get(request):
    return JsonResponse({'types': [
        t.as_dict() for t in PostType.objects.all()
    ]})
