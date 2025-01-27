from django.contrib import admin
from .models import DeliveryRecord

# Register your models here.


class DeliveryRecordAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'mrn', 'name', 'delivery_date', 'managed_by')
    list_display_links = ('mrn',)  # Optional: make 'mrn' a link to the record

# Register the DeliveryRecord model with the new admin class
admin.site.register(DeliveryRecord, DeliveryRecordAdmin)