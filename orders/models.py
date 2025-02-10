from django.db import models


order_choices = (
    ('P', 'Pending'),
    ('OD', 'Out for delivery'),
    ('D', 'Delivered'),
)
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    delivery_person = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='deliveries',limit_choices_to={'is_delivery_person': True})
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10,choices=order_choices)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey('sabji.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.product.name
    
payment_choices = (
    ('P', 'Pending'),
    ('C', 'Completed'),
)

class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)
    payment_uuid = models.CharField(max_length=50)
    status = models.CharField(max_length=10,choices=payment_choices)