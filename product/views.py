from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .cart import Cart
# Create your views here.
# def index(request):
#     return render( request, 'product/index.html')

def product_price(request, id):
    product = get_object_or_404(Product, pk=id)
    total_price = product.price  # Assuming 'price' is a field in your Product model
    return JsonResponse({'product_id': id, 'total_price': total_price})


def cart_summary(request):
    cart=Cart(request)
    products=cart.get_products()
    quantity=cart.get_quantity()
    
    total=cart.get_total_price()
    summa=0
    for product in products:
        summa += cart.get_total_price_for_product(product)
    data={
         'products':products,
         'quantites':quantity,
         'total':total,
         'summa':summa
    }
         
    return render(request, 'product/cart_summary.html', context=data)
 
def cart_add(request):
        cart=Cart(request)
        
        if request.POST.get('action') == 'post':
            product_id=int(request.POST.get('product_id'))
            quantity=request.POST.get('product_quantity')
            product=get_object_or_404(Product, id=product_id)
            cart.add(product=product, quantity=quantity)

        return JsonResponse({'product_id':product_id})

   

def cart_update(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id=int(request.POST.get('product_id'))
        quantity=request.POST.get('product_quantity')
        product=get_object_or_404(Product, id=product_id)
        cart.product_update(product,quantity)
    return JsonResponse({'status':'Hello world'})

def cart_delete(request):
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        print(request.POST)
        product_id = request.POST.get('product_id')
        cart.delete_product(product_id)
        return JsonResponse({'status': 'salom'})


class ProductListView(ListView):
    model=Product
    template_name='product/index.html'
    context_object_name='products'

    
class CategoryProductList(DetailView):
    model=Category
    template_name='product/index.html'
    context_object_name='products'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        context['products'] = category.products.all()
        return context

def About(request, id):
    category=Category.objects.all()
    product=get_object_or_404(Product, pk=id)

    data={
        'category': category,
        'product': product
    }

    return render(request, 'product/about.html' , context=data)