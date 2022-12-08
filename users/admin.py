from django.contrib import admin
from .models import Faction, Profile, Channel
# Register your models here.

myModels = [Faction, Profile, Channel]
admin.site.register(myModels)

