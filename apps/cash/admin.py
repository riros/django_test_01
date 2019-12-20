from django.contrib import admin

# Register your models here.
from apps.cash.models import CashTransaciton


@admin.register(CashTransaciton)
class AuthorAdmin(admin.ModelAdmin):
    pass
