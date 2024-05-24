from django.shortcuts import render
from .models import PlayVideo, ClearValue, Script, Feedback

# Create your views here.

def home(request):
    videos = PlayVideo.objects.all()
    clear_values = ClearValue.objects.all()
    scripts = Script.objects.all()
    feedbacks = Feedback.objects.all()
    return render (request, "mario/home.html",{
        'videos': videos,
        'clear_values': clear_values,
        'scripts': scripts,
        'feedbacks': feedbacks
    })
