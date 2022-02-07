from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.TextField(verbose_name = "Заголовок")
    content = models.TextField(verbose_name = "Текст новости", null = True, blank = True)
    published = models.DateTimeField(verbose_name = "Дата публикации", null = True, blank = True, db_index = True)
    saved = models.DataTimeField(verbose_name = "Дата сохранения", auto_now_add = True, editable = False)
    link = models.URLField(verbose_name = "Ссылка на оригинал", null = True, blank = True)
    tags = models.ManyToManyField(Tag)
    users = models.ManyToManyField(User)
    is_deleted = models.BoleanField(verbose_name = "Активность", default = True, editable = False)
    class Meta:
        verbose_name = "Новость"
        unique_together = ('title', 'link')   
    
 class Tag(models.Model):
    tag = models.CharField(max_length = 50, verbose_name = "Категория")
    class Meta:
        verose_name = "Категория"
        
 class Site(models.Model):
    name = models.CharField(max_length = 50, verbose_name = "Название источника")
    link = models.URLField(verbose_name = "Адрес источника")
    users = models.ManyToManyField(User)
    articles = models.ManyToManyField(Article)
    is_active = models.BoleanField(verbose_name = "Активность", default = False)
    class Meta:
        verbose_name = "Источник"
