from django.contrib import admin
from .models import User, AgentProfile

# Register your models here.

admin.site.register(User)
admin.site.register(AgentProfile)