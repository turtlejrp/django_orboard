from django.contrib import admin
from dashboard.models import PartNO, Cycletime
from lossreport.models import Loss

# Register your models here.
admin.site.site_header = 'OR Board'


class CycletimeAdmin(admin.ModelAdmin):
    list_display = ['partno', 'create_at_time', 'create_at_date']


class PartnoAdmin(admin.ModelAdmin):
    list_display = ['partnumber', 'cycletime']

class LossAdmin(admin.ModelAdmin):
    list_display = ['problem', 'lossType','duration','create_at_date','create_at_time']



admin.site.register(Cycletime, CycletimeAdmin)
admin.site.register(PartNO, PartnoAdmin)
admin.site.register(Loss,LossAdmin)
