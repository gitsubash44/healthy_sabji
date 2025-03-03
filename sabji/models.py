from django.db import models
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(help_text='Price per kilo')
    pre_discount_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products',null=True)


    def __str__(self):
        return f'{self.name} - {self.price} - {self.quantity}'
    
    def get_absolute_url(self):
        return reverse('productDetail', args=[str(self.id)])
    
    def increase_quantity(self, quantity):
        self.quantity += quantity
        self.save()

    def decrease_quantity(self, quantity):
        self.quantity -= quantity
        self.save()

    def is_available(self):
        return self.quantity > 0
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)
    

class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        pass
    