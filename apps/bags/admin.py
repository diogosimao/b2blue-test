from django.contrib import admin

from .models import Bag, Measure, CSVFile


@admin.register(Bag)
class BagAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(CSVFile)
class CSVFileAdmin(admin.ModelAdmin):
    exclude = ('slug',)
