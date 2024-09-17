from django.contrib import admin
from user.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'address', 'phone', 'city', 'country', 'currency', 'image_tag']
    # Removed 'language' as it's no longer part of UserProfile

admin.site.register(UserProfile, UserProfileAdmin)
