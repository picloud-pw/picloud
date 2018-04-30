from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('cloud')
    else:
        return redirect('about')


def about(request):
    return render(request, 'index.html')
