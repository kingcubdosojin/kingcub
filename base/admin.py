from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Order)
admin.site.register(Quote)
admin.site.register(Shipper)
admin.site.register(MailError)
admin.site.register(TempUser)
admin.site.register(Receiver)