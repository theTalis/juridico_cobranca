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
    path('pagamento', pagamento, name="pagamento"),
    path('acordo', acordo, name="acordo"),
    path('juridico_externo', juridico_externo, name="juridico_externo"),
    path('logout', logout, name="logout"),

    path('update_checked', update_checked, name="update_checked"),

    path('submit_cadastro', submit_cadastro, name="submit_cadastro"),
    path('submit_importacao', submit_importacao, name="submit_importacao"),
    path('submit_update_titulo', submit_update_titulo, name="submit_update_titulo"),

    path('submit_update_pagamento', submit_update_pagamento, name="submit_update_pagamento"),
    path('submit_update_acordo', submit_update_acordo, name="submit_update_acordo"),
    path('submit_update_juridico_externo', submit_update_juridico_externo, name="submit_update_juridico_externo"),
    path('submit_update_observacoes', submit_update_observacoes, name="submit_update_observacoes"),
    path('submit_update_observacoes_acordo', submit_update_observacoes_acordo, name="submit_update_observacoes_acordo"),

    path('submit_pagamento_parcial', submit_pagamento_parcial, name="submit_pagamento_parcial"),
    path('submit_pagamento_parcial_acordo', submit_pagamento_parcial_acordo, name="submit_pagamento_parcial_acordo"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
