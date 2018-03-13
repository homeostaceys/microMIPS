from django.contrib import admin
from .models import Codes
from .models import Opcodetable
from .models import Registers
from .models import Memory
# Register your models here.

admin.site.register(Codes)
admin.site.register(Opcodetable)
admin.site.register(Registers)
admin.site.register(Memory)