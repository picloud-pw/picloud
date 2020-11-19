import operator
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse

from posts.models import Post


def search(request):
    query = request.GET.get('q', None)

    if query is None:
        return JsonResponse([], safe=False)
    query = " ".join(query.split())
    query = query.strip()
    words = query.split()

    posts = Post.objects.filter(is_approved=True)
    posts = posts.filter(reduce(operator.or_, (Q(title__icontains=x) for x in words)))
    posts = posts.order_by('-created_date')[:10]

    return JsonResponse({'results': {
        'posts': [post.as_dict() for post in posts],
    }})
