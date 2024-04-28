from django.contrib import admin
from .models import ParsedData,RegisterReadings

# Register your models here.
admin.site.register(ParsedData)
admin.site.register(RegisterReadings)