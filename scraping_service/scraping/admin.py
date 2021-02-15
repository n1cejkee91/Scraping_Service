from django.contrib import admin
from .models import City, Languages, Vacancy


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class LanguagesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(City, CityAdmin)
admin.site.register(Languages, LanguagesAdmin)
admin.site.register(Vacancy)
