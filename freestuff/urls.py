from django.urls import path

from . import views


app_name = 'freestuff'

urlpatterns = [
    path('', views.things_list, name='things_list'),
    path('things/<int:category_pk>/<slug:category_slug>/', views.things_list, name='things_list_by_category'),
    path('thing/<int:pk>/<slug:slug>/', views.thing_detail, name='thing_detail'),
]
