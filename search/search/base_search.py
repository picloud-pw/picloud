from abc import abstractmethod

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator


class BaseSearch:

    def __init__(self, search_type, page, page_size):
        self.page = page
        self.search_type = search_type
        self.page_size = page_size

    @abstractmethod
    def search(self, query): pass

    def paging(self, results):
        paginator = Paginator(results, self.page_size)
        try:
            page = paginator.page(self.page)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        return page
