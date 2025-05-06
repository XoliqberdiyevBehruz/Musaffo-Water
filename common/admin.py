from django.contrib import admin

from common import models 


class ClientPhoneNumberInline(admin.TabularInline):
    model = models.ClientPhoneNumber
    extra = 0


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'code_number', 'full_name']
    inlines = [ClientPhoneNumberInline]
    search_fields = ['full_name', 'code_number']

@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'count', 'client']
    autocomplete_fields = ['client']


@admin.register(models.NumberOfTrips)
class NumberOfTripsAdmin(admin.ModelAdmin):
    list_display = ['id', 'number']
    autocomplete_fields = ['client']