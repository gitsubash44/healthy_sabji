from django.db import models

order_choices = (
    ('P', 'Pending'),
    ('OD', 'Out for delivery'),
    ('D', 'Delivered'),
)
# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE)
    delivery_person = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='deliveries',limit_choices_to={'is_delivery_person': True},null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey('Location', on_delete=models.CASCADE,null=True, blank=True)
    status = models.CharField(max_length=10,choices=order_choices)
    payment = models.ForeignKey('Payment', on_delete=models.CASCADE, null=True, blank=True)
    evidence = models.ImageField(upload_to='evidence/',null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        if self.status == 'OD' and self.delivery_person is None:
            raise ValueError('Delivery person is required for out for delivery status')
        if self.evidence :
            self.status = 'D'
        super(Order, self).save(*args, **kwargs)

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
    signature = models.CharField(max_length=100,null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=20)
    payment_uuid = models.CharField(max_length=50)
    status = models.CharField(max_length=10,choices=payment_choices)

class Location(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    house_number_street_name = models.CharField(max_length=100)
    city_area = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField()
    order_notes = models.TextField(blank=True)
    
    def __str__(self):
        return self.address + ' ' + self.city_area