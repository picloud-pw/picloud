from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect('feed')
    else:
        return redirect('about')


def robots(request):
    return render(request, 'robots.txt', content_type="text/plain")


def about(request):
    return render(request, 'index.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')
