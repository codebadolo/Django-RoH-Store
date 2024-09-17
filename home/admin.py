from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from home.models import Setting, ContactMessage, FAQ


class SettingAdmin(ModelAdmin):
    list_display = ['title','company', 'update_at','status']

class ContactMessageAdmin(ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

class FAQAdmin(ModelAdmin):
    list_display = ['question', 'answer', 'ordernumber', 'status']  # Removed 'lang'
    list_filter = ['status']  # Removed 'lang'

admin.site.register(Setting, SettingAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(FAQ, FAQAdmin)



