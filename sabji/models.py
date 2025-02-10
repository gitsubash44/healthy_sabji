from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField(help_text='Price per kilo')
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    quantity = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='products',null=True)


    def __str__(self):
        return f'{self.name} - {self.price} - {self.quantity}'
    
    # TODO: add get_absolute_url method
    def get_absolute_url(self):
        pass
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
    