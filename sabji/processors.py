from .models import Product, Category


def productprocessor(request):
    products = Product.objects.filter(quantity__gt=0)
    return {'products': products}


def categoryprocessor(request):
    categories = Category.objects.all()
    return {'categories': categories}