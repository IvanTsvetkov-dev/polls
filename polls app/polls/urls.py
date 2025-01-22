from django.urls import path

from . import views

# Указали пространство имён. Теперь в шаблонах мы можем ссылаться явно на polls:detail
app_name = "polls"
"""
Функция path принимает четыре аргумента - route, view, **kwawrgs, name
route - строка, содержащая шаблог URL
view - когда Django находит соответствующий шаблон, он вызывает указанную функцию представления с объектом HttpRequest в качестве первого аргумента и любые знаения из маршрута
переданные в качестве аргументов.
name - позволяет присвоить имя URL адресу и  ссылаться в дальнейшем на него из других мест Django.
"""
urlpatterns = [
    # /polls/
    path("", views.index, name="index"),
    
    # /polls/5/
    # <преобразователь: название аргумента>
    path("<int:question_id>/", views.detail, name="detail"),
    
    # /polls/5/results
    path("<int:question_id>/results/", views.result, name="results"),
    
    # /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote")
]