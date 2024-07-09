from django.contrib import admin
from .models import devices,packeges,subscriber,transactions,counting,counting_settings
admin.site.register (devices)
admin.site.register(packeges)
admin.site.register(subscriber)
admin.site.register(transactions)
admin.site.register(counting)
admin.site.register(counting_settings)

# Register your models here.
