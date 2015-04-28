from django.contrib import admin

from .models import Sensor, Reading

admin.site.register(Sensor)


class ReadingAdmin(admin.ModelAdmin):
    # ...
    list_display = ('reading', 'reading_date', 'sensor')
    list_filter = ['sensor']

admin.site.register(Reading, ReadingAdmin)