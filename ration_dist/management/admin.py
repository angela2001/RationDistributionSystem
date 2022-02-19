from django.contrib import admin
from management.models import *
# Register your models here.
admin.site.register(RationStore)
admin.site.register(RationCard, RationCardAdmin)
admin.site.register(Dependent)
admin.site.register(Provision)
admin.site.register(Quota)
admin.site.register(Granary)
admin.site.register(StockAcquisition)