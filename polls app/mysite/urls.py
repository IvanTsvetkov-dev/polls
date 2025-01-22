from django.contrib import admin
from django.urls import path, include

"""
Базовый цикл работы маршрутизации в Django:
1. Когда запрашивается страница, например /polls/4/ Django загружает модуль, указанный в settings.py в переменной ROOT_URLCONF в нашем случае это mysite.urls.
2. В данном файле находится переменная urlpatterns, которая является списком маршрутов и ищет совпадение с запрашиваемым шаблоном.
3. Как только находитсовпадение по адресу polls/ то вырезается совпадающий текст и отправляетс оставшийся текст в UrlConf polls.urls для дальнешей обработки.

"""
urlpatterns = [
    path("polls/", include("polls.urls")),
    path('admin/', admin.site.urls),
]
