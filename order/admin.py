from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product', 'quantity']


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['total_sum']
    exclude = ['user']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        obj.total_sum = 0
        obj.save()

    def count_total_sum(self, order):
        total = 0
        for item in order.items.all():
            total = item.product.price * item.quantity
        order.total_sum = total
        order.save()
        return order

    def response_add(self, request, obj, post_url_continue=None):
        order = self.count_total_sum(obj)
        return super().response_add(request, order, post_url_continue)

    def response_change(self, request, obj):
        order = self.count_total_sum(obj)
        return super().response_change(request, order)


admin.site.register(Order, OrderAdmin)

