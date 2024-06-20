from django.db import models
from django.utils import timezone

from users.models import User

class Post(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    created_date = models.DateTimeField(default=timezone.now, verbose_name='Дата создания')
    published_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        db_table = 'post'
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Автор')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, verbose_name='Пост')
    text = models.TextField(verbose_name='Текст')
    published_date = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.user.username} | Пост {self.post.title} | Текст {self.text}'