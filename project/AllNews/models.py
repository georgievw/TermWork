from django.db import models

class Article(models.Model):
    title = models.TextField()
    content = models.TextField()
    published = models.DateTimeField(db_index=True)
    tag = models.CharField(max_length=50)
