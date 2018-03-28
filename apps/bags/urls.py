from django.urls import path

from .views import bag_list


urlpatterns = [
    path('reports/', bag_list, name='reports'),
]
