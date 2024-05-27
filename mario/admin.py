from django.contrib import admin
from .models import PlayVideo, ClearValue, Script, OurFeedback, PlayerFeedback

# Register your models here.

admin.site.register(PlayVideo)
admin.site.register(ClearValue)
admin.site.register(Script)
admin.site.register(OurFeedback)
admin.site.register(PlayerFeedback)