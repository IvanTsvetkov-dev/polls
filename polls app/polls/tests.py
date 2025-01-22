from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() возвращает False для вопроса где дата публикации находится в будущем
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() возвращает False если дата публикации находится в далеком прошлом(>1 дня)
        """
        time = timezone.now() - datetime.timedelta(days=2)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() возвращает True где дата публикации в недавнем прошлом(<= 1 дня)
        """
        time = timezone.now() - datetime.timedelta(hours=8)
        recently_question = Question(pub_date=time)
        self.assertIs(recently_question.was_published_recently(), True)

def create_question(question_text, days):
    """
    Функция для создания объекта Question
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_question(self):
        """
        Если вопросов нет, то отображается сообщение
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])
    
    def test_past_question(self):
        """
        вопросы из прошлого должны отображаться
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )
    def test_future_question(self):
        """
        вопросы из будущего(неопубликованные) не должны отображаться
        """
        question = create_question(question_text="Future question", days = 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            []
        )
    def test_future_question_and_past_question(self):
        """
        Каждый вопрос из прошлого отображается, а из будущего нет
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question]
        )

class QuestionDetailViewTests(TestCase):
    """
    Если вопрос не опубликован, то его варианты ответа нельзя просмотреть
    """
    def test_future_question(self):
        future_question = create_question("Future question.", days=23)
        response = self.client.get(reverse("polls:detail", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
    """
    Если  вопрос опубликован, то его варианты ответа можно посмотреть
    """
    def test_past_question(self):
        past_question = create_question("Past question.", days=-2)
        response = self.client.get(reverse("polls:detail", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)

class QuestionResultsViewTests(TestCase):
    """
    Если вопрос не опубликован, то его результаты нельзя просмотреть
    """
    def test_future_question(self):
        future_question = create_question("Future question.", days=23)
        response = self.client.get(reverse("polls:results", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
    
    """
    Если вопрос не опубликован, то его результаты можно посмотреть
    """
    def test_past_question(self):
        past_question = create_question("Past question.", days=-2)
        response = self.client.get(reverse("polls:results", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)