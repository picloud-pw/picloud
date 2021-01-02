from django.http import JsonResponse

from search.search.base_search import BaseSearch


def search(request):
    query = request.GET.get('q', None)
    search_type = request.GET.get('t')
    page = request.GET.get('p', 1)
    page_size = request.GET.get('ps', 15)

    results = BaseSearch(search_type, page, page_size)\
        .search(query)

    return JsonResponse({'results': results})
