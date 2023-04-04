from django.contrib import admin
from django.urls import path,include
from . import views


urlpatterns = [
    path('index/',views.index,name='index'),
    path('records/', views.view_records, name='view_records'),
    path('delete_record/<int:record_id>/', views.delete_record, name='delete_record'),
]
