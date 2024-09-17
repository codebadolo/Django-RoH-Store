from currencies.models import Currency
from django.contrib.auth.models import User
from django.db import models
from django.utils.safestring import mark_safe

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)  # Currency kept intact

    def __str__(self):
        return self.user.username

    def user_name(self):
        return f'{self.user.first_name} {self.user.last_name} [{self.user.username}]'

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" height="50"/>')
    image_tag.short_description = 'Image'
