from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'legal/privacy_policy.html')
