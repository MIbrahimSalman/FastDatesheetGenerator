from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('datesheet_app.urls')),  # This includes all your app URLs
    path('accounts/', include('django.contrib.auth.urls')),
]
