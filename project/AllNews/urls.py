from django.urls import path

from .views import index, by_site

urlpatterns = [
    path('<int:site_id>/', by_site),
    path('', index),
]
