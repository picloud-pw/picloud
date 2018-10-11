from django.shortcuts import get_object_or_404, render, redirect

from cloud.forms import NewProgramForm
from cloud.models import Program, Subject
from cloud.views.message import message
from cloud.views.posts import can_user_publish_instantly


def program_page(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    subjects = Subject.objects.filter(programs=program).filter(is_approved=True)
    semesters = set()
    for sub in subjects:
        semesters.add(sub.semester)
    return render(request, "structure/program_page.html", {
        "program": program,
        "subjects": subjects,
        "semesters": semesters,
    })


def new_program(request):
    if request.method == "POST":
        success_msg = "Данные успешно сохранены. В ближайшее время они будут проверены модераторами."

        new_program = NewProgramForm(request.POST)
        if new_program.is_valid():
            program = new_program.save(commit=False)
            program.is_approved = can_user_publish_instantly(request.user)
            program.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Программа" заполнено некорректно')
    else:
        new_program = NewProgramForm()
        return render(request, 'structure/new/program.html', {'new_program': new_program})


def program_delete(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        program.delete()
    return redirect("moderation")


def program_approve(request, program_id):
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        Program.objects.filter(pk=program_id).update(is_approved=True)
        return redirect("moderation")
    else:
        return redirect("cloud")
