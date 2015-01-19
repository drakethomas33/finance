from django.contrib import admin

from .models import Transaction, Month, Account, Category


def close_months(modeladmin, request, queryset):
    queryset.update(closed=True)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'amount', 'account', 'category', 'description']
    list_filter = ['account', 'category']


class MonthAdmin(admin.ModelAdmin):
    list_display = ['start', 'end', 'closed']
    actions = [close_months]


class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'initial']


class CategoryAdmin(admin.ModelAdmin):
    actions = []

admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Month, MonthAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Category, CategoryAdmin)
