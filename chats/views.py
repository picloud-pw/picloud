import random
import string

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse

from chats.models import Chat, Message
from decorators import auth_required


@auth_required
def chat_list(request):
    chats = Chat.objects.filter(members__in=[request.user])
    return JsonResponse({'chats': [
        chat.as_dict() for chat in chats
    ]})


@auth_required
def chat_add(request):
    chat_name = request.POST.get(
        'name',
        ''.join(random.sample(string.ascii_lowercase, 10))
    )
    title = request.POST.get('title')
    if title is None or title == '':
        return HttpResponse(status=401, content=f'Required argument (title) unspecified.')
    try:
        Chat.objects.get(name=chat_name)
        return HttpResponse(status=401, content=f'Chat with name "{chat_name}" already exist.')
    except ObjectDoesNotExist:
        new_chat = Chat.objects.create(
            author=request.user,
            title=title,
            name=chat_name,
        )
        new_chat.members.add(request.user)
        return HttpResponse(status=200)


@auth_required
def chat_delete(request):
    chat_name = request.POST.get('chat_name')
    if chat_name is None:
        return HttpResponse(status=401, content=f'Required argument (chat_name) unspecified.')
    try:
        chat = Chat.objects.get(name=chat_name)
        if chat.author == request.user:
            chat.delete()
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=403)
    except ObjectDoesNotExist:
        return HttpResponse(status=402)


@auth_required
def message_list(request):
    chat_name = request.GET.get('chat_name')
    if chat_name is None:
        return HttpResponse(status=403, content=f'Required argument (chat_name) unspecified.')
    try:
        chat = Chat.objects.get(name=chat_name)
        if request.user not in chat.members.all():
            return HttpResponse(status=401, content=f'You have no access.')
        messages = Message.objects.filter(chat=chat).order_by('created')
        return JsonResponse({'messages': [msg.as_dict() for msg in messages]})
    except ObjectDoesNotExist:
        return HttpResponse(status=404, content=f'Chat with name "{chat_name}" does not exist.')


@auth_required
def message_add(request):
    chat_name = request.POST.get('chat_name')
    message = request.POST.get('message')
    if chat_name is None:
        return HttpResponse(status=403, content=f'Required argument (chat_name) unspecified.')
    if message is None or message == '':
        return HttpResponse(status=403, content=f'Required argument (msg) unspecified.')
    try:
        chat = Chat.objects.get(name=chat_name)
        if request.user not in chat.members.all():
            return HttpResponse(status=401, content=f'You have no access.')
        Message.objects.create(
            author=request.user,
            chat=chat,
            text=message,
        )
        return HttpResponse(status=200)
    except ObjectDoesNotExist:
        return HttpResponse(status=404, content=f'Chat with name "{chat_name}" does not exist.')


@auth_required
def message_edit(request):
    pass


@auth_required
def message_delete(request):
    pass
