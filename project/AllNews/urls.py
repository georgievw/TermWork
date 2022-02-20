from django.urls import path, re_path

from .views import index, my_news, my_saved, my_settings

urlpatterns = [
    path('', index),
    path('my_news', my_news),
    path('my_saved', my_saved),
    path('settings', my_settings),
]

