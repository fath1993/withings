from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from accounts.views import index, webhook_listen
from healthcare.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

    path('webhook/', webhook_listen),
    path('auth/', include('accounts.urls')),
    path('data/', include('healthcare.urls')),
    path('home/', dashboard, name='dashboard'),
    path('', index, name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)