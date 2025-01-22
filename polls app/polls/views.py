from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Choice, Question
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import F

# Возвращает страницу с опросами
def index(request):
    # Забираем первые 5 вопросов из базы данных, отсоритрованных по дате публикации
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    # output = ", ".join([q.question_text for q in latest_question_list])
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request=request, template_name="polls/index.html", context=context)
    """
    Поговорим о том, что здесь происходит.
    latest_question_list по прежнему извлекает первые 5 вопросов из базы данных с помощью API.
    В предыдущей реализации html код был захардкожен в HttpResponse, что не является хорошей практикой. Если поместить html код дейсвительно реалной страницы, то мы получим очень очень много кода html внутри python кода.
    Для того, чтобы отделить python код и html код существует template(шаблоны)
    В mysite.setting.py есть параметр TEMPLATES который описывает, как DJANGO будет загружать и отображать шаблоны.
    
    Теперь у нас выполняются следующие шаги:
    1. Загружается HTML шаблон, который находится в polls/templates/polls/index.html
    2. Мы заполняем контекст записями из базы данных.(Помещаем внутри шаблона данные) context = Mapping[str, Any]
    3. Функция render принимает объект запроса, имя шаблона и словарь(контекст) в качестве необязательного третьего аргумента и возвращает HttpResponse
    
    
    """


# Возвращает страницу с деталями опроса 

def detail(request, question_id):
    
    """
    Частой практикой является запрашивать get и в случае несуществыования объекта выдавать 404 ошибку. Есть сокращение get_object_or_404()
    Вместо этого:
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except:
    #     raise Http404("Question does not exist")
    # return render(request, "polls/detail.html", {"question": question})
    """
    # Имеем:
    question = get_object_or_404(Question, pk=question_id)
    return render(request=request, template_name="polls/detail.html", context={"question": question})


def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request=request, template_name="polls/results.html", context={"question": question})

"""
Представление, которое обарабатывает POST запрос с отправленной формой, где выбран
один из вариантов

Нам известен question_id - id голоса.Мы получаем объект и с помощью choice_set.get получаем объект голоса, которому нужно прибавить
счетчик.

объект request.POST содержит в себе словарь, в котором мы можем обратиться по имени нашего вводимого значения, в данном случае choice,
который возвращает первичный ключ Choice.

"""
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(
            request=request,
            template_name="polls/detail.html",
            context={
                "question": question,
                "error_message": "You didn't select a choice"
            }
        )
    else:
        """
        Здесь может возникнуть проблема, которая называется состоянием гонки
        Например, два пользователя извелкли одновременно selected.choice и количество голосов равно 2
        далее инкрементировали значение голосов до 3-х и сохранили это в базе данных. Но ведь в итоге должно быть значение 4, а не 3.
        Для избежения подобных ситуаций в DJANGO используется F()
        Объект F позволяет напрямую работать с базой данных, генерируя SQL выражения для требуемой операции.
        Это поможет избежать ситуцации гонки, когда два потока Python выполняют код и один поток получил и увеличил значение после того, как другой получил значение из базы данных
        В таком случае работа первого потока будет потеряна. А если за обновление поля будет отвечать база данных, то этот процесс будет более надежен:
        значение поля будет обновляться только на основе значения, которое хранится в базе данных при выполнении команды save()
        """
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        """
        HttpResponseRedirect принимает один аргумент: URL адрес, на который будет перенаправлен пользователь
        Всегда требуется после отправки данных POST возвращать redirect, так как это предовтратит повторную отправку формы.
        В конструктор HttpResponseRedirect мы передаём функцию reverse, которая позволяет нам вместо жесктого написания 
        URL-адреса, куда требуется перенаправить пользователя, указать app_name и имя представления, которому мы хотим передать управление
        функция reverse вернёт следующую строку: polls/question.id/results
        
        """
        return HttpResponseRedirect(reverse("polls:results", args=[question.id]))