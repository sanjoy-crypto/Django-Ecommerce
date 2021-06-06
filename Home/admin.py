from django.contrib import admin
from .models import *
# Register your models here.

admin.site.site_header = "SarkerFashion"


class SettingAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'status', 'update_at']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'status', 'subject', 'create_at']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'status']
    list_filter = ['status']


admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(SliderImage)
admin.site.register(OfferImage)
admin.site.register(FAQ, FAQAdmin)
