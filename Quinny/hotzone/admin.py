from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Patient)
admin.site.register(Virus)
admin.site.register(LocationVisited)
admin.site.register(Case)
