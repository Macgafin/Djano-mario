from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('information/', views.information, name='information'),  # informationビューへのパスを追加
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
