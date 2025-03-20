from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_datesheet, name='upload_datesheet'),
    path('datesheet/', views.display_datesheet, name='datesheet'),
    path('download/', views.download_datesheet, name='download_datesheet'),
]
