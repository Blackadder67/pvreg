from django.shortcuts import render, get_object_or_404
from .models import Person, Department, Product, Exam, Question, Answer
from django.db.models import Q
from django.core.mail import send_mail
from random import sample
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import Http404
from django.utils.timezone import now as NOW

# Create your views here.

def index_view(request):
    return render(request, 'app/index.html')

def contacts_search_view(request):
    departments = Department.objects.all()
    return render(request, 'app/contacts_search.html', {'departments': departments})

def contacts_view(request):
    contact_search = request.POST.get('contact_search')
    people = Person.objects.filter(Q(lname__contains=contact_search) | Q(fname__contains=contact_search)).order_by('lname')
    return render(request, 'app/contacts.html', {'people': people})

def department_contacts_view(request):
    dep = request.POST.get('department')
    people = Department.objects.get(pk=dep).get_people()
    return render(request, 'app/contacts.html', {'people': people})

def pv_view(request):
    return render(request, 'app/pv.html')

def psur_view(request):
    return render(request, 'app/psur.html')

def ct_view(request):
    return render(request, 'app/ct.html')

def reg_view(request):
    return render(request, 'app/reg.html')

def products_view(request):
    products = Product.objects.all()
    return render(request, 'app/products.html', {'products': products})

def product_details_view(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'app/products.html', {'product': product})


def starttesting_view(request):
    return render(request, 'app/starttesting.html')

def check_pass_view(request):
    #количество вопросов в тесте
    questionnaire_size = 5
    #exam = None
    keyword = request.POST.get('inputKeyword')
    try:
        exam = Exam.objects.get(guid=keyword)
    except:
        return Http404

    #если тест уже сдавался и балл выше 80%
    if exam.rate != None and exam.rate >= 80:
        return render(request, 'app/already_ok.html', {'exam': exam})

    questions = sample(list(Question.objects.all()), questionnaire_size)
    answers_pks = []
    for q in questions:
        for a in q.get_answers():
            answers_pks.append(a.pk)
    request.session['guid'] = keyword
    #request.session['email'] = exam.person.email
    request.session['answers_pks'] = answers_pks
    request.session['questionnaire_size'] = questionnaire_size
    request.session.save()
    return render(request, 'app/welcome_to_test.html', {'exam': exam, 'questions': questions} )

def result_view(request):
    checked_answers = request.POST.getlist('chbox')
    answers_pks = request.session['answers_pks']

    max_points = request.session['questionnaire_size']
    #PK заданных вопросов
    wrong_answered_questions = []
    #перебираем все варианты ответов
    for ap in answers_pks:
        a = Answer.objects.get(pk=ap)
        #если правильный вариант и отмеченный юзером не совпадают
        if a.is_correct != (str(a.pk) in checked_answers):
            #берем РК вопроса, в котором юзер допустил ошибку
            current_question_pk = a.question.pk
            #если неправильно отвеченный вопрос еще не вставлен в массив неправильно отвеченных
            #(чтобы не записывать несколько раз одно и то же)
            if not current_question_pk in wrong_answered_questions:
                #тогда записываем РК неправльно отвеченного в массив
                wrong_answered_questions.append(current_question_pk)
                #количество правильно отвеченных = количество заданных вопросов минус количество неправильных
    point = max_points - len(wrong_answered_questions)

    keyword = request.session['guid']
    exam = Exam.objects.get(guid=keyword)
    email = exam.person.email

    exam.rate = round((point / max_points) * 100)
    exam.save()


    #если юзер ответил на 80% вопросов
    if exam.rate >= 80:
        exam.resolved = datetime.now()
        exam.save()
        try:
            send_mail(
                'Результат теста по фармаконадзору',
                'Пользователь {e} прошел тест с результатом {r}%'.format(e = exam.person.email, r = exam.rate),
                'spilpv@mail.ru',
                ['Alexey.Oberemkov@sunpharma.com', 'Marina.Tabulova@sunpharma.com'],
                fail_silently=False
            )
        except:
            pass
    return render(request, 'app/result.html', {'point': point, 'max_points': max_points, 'email': email})

@login_required
def allpeople_view(request):
    try:
        people = Person.objects.filter(active=True).order_by('email')
        return render(request, 'app/allpeople.html', {'people': people})
    except:
        return render(request, 'app/authentication_required.html')

def exams_created_shared_view(request):
    people_pks_to_receive_emails = request.POST.getlist('chbox')

    for p in people_pks_to_receive_emails:

        person_to_receive_email = Person.objects.get(pk=int(p))
        exam = Exam()
        exam.person = person_to_receive_email
        exam.set_guid()
        exam.save()

        #ip_address = 'http://192.168.0.188:8000'
        ip_address = 'www.sunpv-portal.ru'

        # try:
        success = send_mail(
            'Тест по фармаконадзору',
            'Уважаемый пользователь {}!\nВам предлагается пройти тест по фармаконадзору.\nСсылка на сайт: {} \nВаш персональный код для входа на сайт: \n{}\n\nЕсли ссылка не открывается, ее можно скопировать/вставить в адресную строку браузера\n\nТест считается пройденным при 80% правильных ответов'.format(exam.person.email, ip_address, exam.guid),
            'spilpv@mail.ru',
            [exam.person.email],
            fail_silently=False
        )
        send_mail(
            'PV Test sent to: {}'.format(exam.person.email),
            'Тест по фармаконадзору выслан на адрес {}'.format(exam.person.email),
            'spilpv@mail.ru',
            ['Alexey.Oberemkov@sunpharma.com', 'Marina.Tabulova@sunpharma.com'],
            fail_silently=False
        )
        if success == 1:
            exam.sent = datetime.now()
        exam.save()
        # except:
        #     pass

        exam.save()
        num_of_people_received_test = 0
        try:
            num_of_people_received_test = len(people_pks_to_receive_emails)
        except:
            pass
    return render(request, 'app/exams_sent.html', {'people_number':  num_of_people_received_test})

