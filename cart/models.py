from django.db import models

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('sabji.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.product.name
    
    def total_price(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        if self.quantity <= 0:
            return self.delete()
        super(Cart, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        pass

    class Meta:
        unique_together = ('user', 'product')   
