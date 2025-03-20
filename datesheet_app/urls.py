from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_datesheet, name='upload_datesheet'),
    path('datesheet/', views.display_datesheet, name='display_datesheet'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('add_exam/', views.add_exam, name='add_exam'),
    path('delete_exam/', views.delete_exam, name='delete_exam'),
    path('download/', views.download_datesheet, name='download_datesheet'),
]
