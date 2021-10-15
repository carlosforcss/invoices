# -*- coding: utf-8 -*-
# Django
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# Third Parties
# - - -
# Project


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/inventory/', include(('apps.inventory.urls', "inventory", ))),
    path('api/sales/', include(('apps.sales.urls', "sales", ))),
    path('', include(('apps.ui.urls', "ui", ))),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
