from django.http import JsonResponse

from decorators import auth_required
from .models import StudentInfo


@auth_required
def me(request):
    user_info = StudentInfo.objects.get(user=request.user)
    return JsonResponse(user_info.as_dict())
