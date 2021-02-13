from django.contrib import admin
from .models import City, Professions, Vacancy


class CityAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class ProfessionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(City, CityAdmin)
admin.site.register(Professions, ProfessionAdmin)
admin.site.register(Vacancy)
