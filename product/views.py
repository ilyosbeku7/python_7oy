from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .cart import Cart
# Create your views here.
# def index(request):
#     return render( request, 'product/index.html')

def cart_summary(request):
    return HttpResponse('Hello world')
 
def cart_add(request):
        cart=Cart(request)
        product_id=int(request.POST.get('product_id'))
        product=get_object_or_404(Product, id=product_id)
        cart.add(product=product)

        return JsonResponse({'product_id':product_id})

   

def cart_update(request):
    return HttpResponse('Hello world')

def cart_delete(request):
    return HttpResponse('Hello world')

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