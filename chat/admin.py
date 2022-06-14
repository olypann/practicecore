from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Word)
admin.site.register(Game)
admin.site.register(GameWord)