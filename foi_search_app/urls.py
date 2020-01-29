from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('view/<data_id>', views.view, name='view'),
    path('stats', views.stats, name='stats'),
]
