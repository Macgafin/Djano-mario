from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('image_details/', views.image_details, name='image_details'),  # image_details,ビューへのパスを追加
]
