from django.contrib import admin
from .models import *

admin.site.register(VirusDetail)
admin.site.register(PatientDetail)
admin.site.register(CaseDetail)
admin.site.register(VisitedLocationDetail)
admin.site.register(LocationDetail)