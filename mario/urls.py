from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import stream_view

urlpatterns = [
    path('', views.home, name='home'),
    path('video/', stream_view, name='video_stream'),
    path('image_details/', views.image_details, name='image_details'),  # image_details,ビューへのパスを追加
    path('questionnaire/', views.questionnaire, name='questionnaire'),
    path('questionnaire_middle/', views.questionnaire_middle, name='questionnaire_middle'),
    path('submit_feedback', views.submit_feedback, name='submit_feedback'),
    path('submit_experience', views.submit_experience, name='submit_experience'),
]
