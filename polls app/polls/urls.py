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
    path("", views.IndexView.as_view(), name="index"),
    
    # /polls/5/
    # <преобразователь: название аргумента>
    # параметр с question_id был изменён на pk, так как общее представление DetailView ожидает, что будет передан параметр pk
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    
    # /polls/5/results
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    
    # /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote")
]