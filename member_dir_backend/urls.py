from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include('admin_login.urls')),
    path('directory/', include('directory.urls')),
    path('', include('admin_login.urls')),

]