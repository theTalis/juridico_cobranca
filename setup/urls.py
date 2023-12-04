from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from home.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('login', login, name="login"),
    path('submit_login', submit_login, name="submit_login"),
    path('cadastro', cadastro, name="cadastro"),
    path('importacao', importacao, name="importacao"),
    path('logout', logout, name="logout"),

    path('submit_cadastro', submit_cadastro, name="submit_cadastro"),
    path('submit_importacao', submit_importacao, name="submit_importacao"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
