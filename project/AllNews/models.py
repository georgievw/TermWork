from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
   tag = models.CharField(max_length = 50, verbose_name = "Категория")
   
   def __str__(self):
       return self.tag
       
   class Meta:
       verbose_name = "Тег"
       verbose_name_plural = "Теги"
       
class Article(models.Model):
    title = models.TextField(verbose_name = "Заголовок")
    content = models.TextField(verbose_name = "Текст новости", null = True, blank = True, default = "Читайте полный текст в источнике")
    published = models.DateTimeField(verbose_name = "Дата публикации", null = True, blank = True, db_index = True, editable=False)
    saved = models.DateTimeField(verbose_name = "Дата сохранения", auto_now_add = True)
    link = models.URLField(verbose_name = "Ссылка на оригинал", null = True, blank = True)
    tags = models.ManyToManyField(Tag)
    site = models.ForeignKey('Site', default = 0, null = True, on_delete=models.PROTECT)
    users = models.ManyToManyField(User)
    is_deleted = models.BooleanField(verbose_name = "Активность", default = True, editable = False)
    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ["-published"]
        unique_together = ('title', 'link')   
           
class Site(models.Model):
   name = models.CharField(max_length = 50, verbose_name = "Название источника")
   link = models.URLField(verbose_name = "Адрес источника", unique=True)
   users = models.ManyToManyField(User)
   is_active = models.BooleanField(verbose_name = "Активность", default = False)
   is_allowed = models.BooleanField(verbose_name = "Подтверждение администратора", default=True)
   
   def __str__(self):
       return self.name
       
   class Meta:
       verbose_name = "Источник"
       verbose_name_plural = "Источники"
       ordering = ["name"]
