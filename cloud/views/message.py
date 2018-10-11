from django.shortcuts import render


def message(request, msg):
    return render(request, 'message.html', {'message': msg})
