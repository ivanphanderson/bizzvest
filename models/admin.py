from django.contrib import admin

# Register your models here.
from models.models import UserAccount, InvestorAccountData, EntrepreneurAccountData, Company, Comment, Stock


# class UserAccountAdmin(admin.ModelAdmin):
#     list_display = ("first_name", "last_name")


admin.site.register(Comment)
admin.site.register(Company)
admin.site.register(EntrepreneurAccountData)
admin.site.register(InvestorAccountData)
admin.site.register(Stock)
admin.site.register(UserAccount)
