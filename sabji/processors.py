from .models import Product, Category


def productprocessor(request):
    products = Product.objects.filter(quantity__gt=0)
    lowest_price = products.filter(quantity__gt=0).order_by('price').first()
    return {'products': products, 'lowest_price': lowest_price}


def categoryprocessor(request):
    categories = Category.objects.all()
    return {'categories': categories}