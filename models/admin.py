from django.contrib import admin

# Register your models here.
from models.models import UserAccount

class UserAccountAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name")


admin.site.register(UserAccount, UserAccountAdmin)
