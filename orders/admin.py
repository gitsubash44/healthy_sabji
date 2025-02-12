from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('user', 'order_date', 'status')
    list_filter = ('status', 'order_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email')
    date_hierarchy = 'order_date'
    ordering = ('order_date',)
    readonly_fields = ('order_date',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Payment)