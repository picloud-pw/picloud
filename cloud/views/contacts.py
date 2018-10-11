from django.core.mail import EmailMessage
from django.shortcuts import render

from cloud.forms import ContactForm


def contacts(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['contact_name']
            email = form.cleaned_data['contact_email']
            subject = form.cleaned_data['subject']
            content = form.cleaned_data['content']
            mail_msg = content + " <<< " + email + " >>>" + "(((" + name + ")))"
            email = EmailMessage(subject, mail_msg, email, to=["itmo.cloud@gmail.com"])
            email.send()
            msg = "Спасибо! Письмо отправлено. Ваше обращение будет рассмотрено в ближайшее время."
            return render(request, 'message.html', {'message': msg})
        else:
            msg = "Форма заполнена неправильно. Письмо не было отправлено."
            return render(request, 'message.html', {'message': msg})
    else:
        form = ContactForm()
        return render(request, 'contacts.html', {'form': form})
