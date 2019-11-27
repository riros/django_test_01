from django.contrib import admin

from api.models import EUser, CashTransaciton


# Register your models here.


@admin.register(EUser)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(CashTransaciton)
class AuthorAdmin(admin.ModelAdmin):
    pass
