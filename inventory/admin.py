from django.contrib import admin
from .models import Product, StockIn, StockOut, TransactionHistory, ActivityLog, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'pet', 'category', 'price', 'stock', 'stock_status']
    list_filter = ['pet', 'category']
    search_fields = ['name']

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ['username', 'user_role', 'activity_type', 'product_name', 'timestamp']
    list_filter = ['activity_type', 'user_role']
    readonly_fields = ['timestamp']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

admin.site.register(StockIn)
admin.site.register(StockOut)
admin.site.register(TransactionHistory)
