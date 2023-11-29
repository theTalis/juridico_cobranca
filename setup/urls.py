from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('submit_login', submit_login, name="submit_login"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
