from django.shortcuts import render_to_response


def robots(request):
    return render_to_response('robots.txt', content_type="text/plain")
