from django.contrib import admin
from .models import Asset, Category, Location, Transaction, Stocktake
@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('code','name','category','quantity','status','location')
    search_fields = ('code','name','serial_number')
    list_filter = ('status','category','location')
admin.site.register([Category, Location, Transaction, Stocktake])
