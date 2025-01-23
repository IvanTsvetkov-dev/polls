from django.contrib import admin
from .models import Question, Choice

"""
Эффективный интерфейс для добавления связных объектов
Отображаем варианты в удобдном табличном варианте
"""
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_text"]
    """
    Добавляем объекты Choice на странице создания вопроса
    """
    inlines=[ChoiceInline]
    
    # Можно настроить отображение списка объектов, вместо стандартного __str__. По полям можно будет удобно отсортироваь объекты
    list_display = ["question_text", "pub_date"]
    
    # Добавление боковой панели Фильтр
    list_filter = ["pub_date"]
    
    # Добавление возможностей поиска
    search_fields = ["question_text"]    

admin.site.register(Question, QuestionAdmin)