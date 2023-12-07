from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(FullTime)
admin.site.register(Contract)
admin.site.register(Client)

