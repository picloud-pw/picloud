from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect("post_list")
    else:
        return render(request, 'index.html', {})
