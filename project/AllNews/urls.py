from django.urls import path, re_path

from .views import index, by_site, by_tags

urlpatterns = [
    path('tags/0/0/', index),
    path('tags/<int:tag1_id>/<int:tag2_id>/', by_tags),
    path('sites/<int:site_id>/', by_site),  
    path('', index), 
    #path('my_news', my_news)
]
