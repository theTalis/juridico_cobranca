from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('submit_login', submit_login, name="submit_login"),
    path('logout', logout, name="logout"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
