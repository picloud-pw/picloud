from django.shortcuts import get_object_or_404, render

from cloud.forms import NewProgramForm
from cloud.models import Program, Subject
from cloud.views import VALID, NOT_VALID
from cloud.views.message import message


def program_page(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    subjects = Subject.objects.filter(programs=program).filter(validate_status=VALID)
    semesters = set()
    for sub in subjects:
        semesters.add(sub.semestr)
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
            program.validate_status = NOT_VALID
            program.save()
            return message(request, success_msg)
        else:
            return message(request, 'Одно из полей формы "Программа" заполнено некорректно')
    else:
        new_program = NewProgramForm()
        return render(request, 'structure/new/program.html', {'new_program': new_program})
