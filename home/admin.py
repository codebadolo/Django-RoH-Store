
from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from home.models import Setting, ContactMessage, FAQ, Language, SettingLang


class SettingtAdmin(ModelAdmin):
    list_display = ['title','company', 'update_at','status']

class ContactMessageAdmin(ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

class FAQAdmin(ModelAdmin):
    list_display = ['question', 'answer','ordernumber','lang','status']
    list_filter = ['status','lang']

class LanguagesAdmin(ModelAdmin):
    list_display = ['name', 'code','status']
    list_filter = ['status']


class SettingLangAdmin(ModelAdmin):
    list_display = ['title', 'keywords','description','lang']
    list_filter = ['lang']

admin.site.register(Setting,SettingtAdmin)
admin.site.register(SettingLang,SettingLangAdmin)
admin.site.register(ContactMessage,ContactMessageAdmin)
admin.site.register(FAQ,FAQAdmin)
admin.site.register(Language,LanguagesAdmin)


