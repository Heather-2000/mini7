from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def index(request):
    login_cookies = request.COOKIES.get('login', 'None')
    context = {'login_cookies': login_cookies}
    return render(request, 'index.html', context)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('chatgpt/', include('chatgpt.urls')),
    path('selfchatgpt/', include('selfchatgpt.urls')),
    path('login/', include('login.urls')),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
