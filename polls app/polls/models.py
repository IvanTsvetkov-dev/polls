from django.db import models
from django.utils import timezone
import datetime
"""
Каждая модель является наследником django.db.models.Model.

Каждое поле представлено экземпляром класса Field, например CharField - для символьных полей. Это поможет Django понять, какой тип данных содержит поле.
Имя каждого экземпляра Field (например, question_text или pub_date) это название столбика в базе данных.
Необязательный первый позиционный аргумент для Field служит, для обозначения понятного названия, например как в pub_date
"""

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    # Мы можем переопределеить __str__ для того, чтобы выводить нужно нам представление объекта. В данном случае - текст опроса
    def __str__(self):
        return self.question_text
    # Добавили пользовательский метод был ли опубликован вопрос недавно?
    def was_published_recently(self):
        now = timezone.now()
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        return self.pub_date >= now - datetime.timedelta(days=1) and self.pub_date <= now
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text