from django.contrib import admin
from base.models import EUser


# Register your models here.
@admin.register(EUser)
class AuthorAdmin(admin.ModelAdmin):
    pass
