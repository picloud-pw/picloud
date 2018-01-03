from django.shortcuts import render

def post_list(request):
    return render(request, 'cloud/post_list.html', {})
