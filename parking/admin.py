from django.contrib import admin
from .models import devices,packeges,subscriber,transactions,counting

admin.site.register (devices)
admin.site.register(packeges)
admin.site.register(subscriber)
admin.site.register(transactions)
admin.site.register(counting)
# Register your models here.
