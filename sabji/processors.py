from .models import Product, Category


def productprocessor(request):
    products = Product.objects.filter(quantity__gt=0)
    lowest_price = products.filter(quantity__gt=0).order_by('price').first()
    return {'products': products, 'lowest_price': lowest_price}


def categoryprocessor(request):
    categories = Category.objects.all()
    return {'categories': categories}


def discountprocessor(request):
    discounted_products = Product.objects.filter(pre_discount_price__gt=0)
    return {'discounted_products': discounted_products}


def cartprocessor(request):
    cart_count = 0
    if request.user.is_authenticated:
        cart_count = request.user.cart_items.filter(active=True).count()
    return {'cart_count': cart_count}