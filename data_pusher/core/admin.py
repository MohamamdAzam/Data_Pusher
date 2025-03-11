from django.contrib import admin
from .models import Account, Destination

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'app_secret_token')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('account', 'url', 'http_method')
