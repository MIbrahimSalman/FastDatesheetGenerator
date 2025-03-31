from django.contrib import admin
from django.urls import path, include
from datesheet_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.display_datesheet, name='home'),
    path('datesheet/', views.datesheet_view, name='datesheet'),
    path('search_courses/', views.search_courses, name='search_courses'),
    path('add_exam/', views.add_exam, name='add_exam'),
    path('delete_exam/', views.delete_exam, name='delete_exam'),
    path('download/', views.download_datesheet, name='download_datesheet'),
    path('accounts/', include('django.contrib.auth.urls')),
]
