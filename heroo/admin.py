from django.contrib import admin
from .models import Note
# Register your models here.


class YourModelAdmin(admin.ModelAdmin):
    readonly_fields = ('self_d',)


admin.site.register(Note, YourModelAdmin)
