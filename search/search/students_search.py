from search.search.base_search import BaseSearch
from students.models import StudentInfo


class StudentsSearch(BaseSearch):

    def search(self, query):
        students = StudentInfo.objects.all()
        if query is not None:
            students = students.filter(user__username__icontains=query)
        return students
