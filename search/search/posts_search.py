import operator
from functools import reduce

from django.db.models import Q

from posts.models import Post
from search.search.base_search import BaseSearch


class PostsSearch(BaseSearch):

    def search(self, query):
        query = " ".join(query.split())
        query = query.strip()
        words = query.split()

        posts = Post.objects.filter(is_approved=True)
        posts = posts.filter(reduce(operator.or_, (Q(title__icontains=x) for x in words)))
        posts = posts.order_by('-created_date')[:10]
        return posts
