from django.contrib import admin
from .models import *



admin.site.site_title = "Moscow Secure Traffic Service"
admin.site.site_header = "Moscow Secure Traffic Service"



admin.site.register(DetCoords)
admin.site.register(Detectors)
admin.site.register(Fvf)
admin.site.register(Sensors)