from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    content = models.TextField('Содержание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='Автор'
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
    
    def __str__(self):
        return f"{self.title} ({self.user.username})"
