from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    content = models.CharField(max_length=500, blank=True, null=True, verbose_name='Текст сообщения')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='senders', verbose_name='Отправитель')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipients', verbose_name='Получатель')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, null=True, verbose_name='Пост')


CATEGORY = [
    ('TNK', 'Танки'),
    ('HLS', 'Хилы'),
    ('DMG', 'ДД'),
    ('TRD', 'Торговцы'),
    ('GMS', 'Гилдмастеры'),
    ('QST', 'Квестгиверы'),
    ('SMT', 'Кузнецы'),
    ('LTH', 'Кожевники'),
    ('PTN', 'Зельевары'),
    ('SPL', 'Мастера заклинаний'),
]


class Post(models.Model):
    header = models.CharField(max_length=256, blank=True, null=True, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст сообщения')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    category = models.CharField(max_length=3, choices=CATEGORY, verbose_name='Категория')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')