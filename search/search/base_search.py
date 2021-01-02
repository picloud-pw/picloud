from abc import abstractmethod


class BaseSearch:

    def __init__(self, search_type, page, page_size):
        self.page = page
        self.search_type = search_type
        self.page_size = page_size

    @abstractmethod
    def search(self, query): pass
