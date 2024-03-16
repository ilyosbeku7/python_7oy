from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, TemplateView
from .models import Product, Category, Order, OrderItem
from student.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from .cart import Cart
import uuid
from django.core.exceptions import ValidationError
from .telegrambot_message import main
import asyncio
import requests


def product_price(request, id):
    product = get_object_or_404(Product, pk=id)
    total_price = product.price 
    return JsonResponse({'product_id': id, 'total_price': total_price})

def cart_summary(request):
    cart=Cart(request)
    products=cart.get_products()
    quantity=cart.get_quantity()
    all_product=cart.get_all_info()
    total=cart.get_total_price()
   
    data={
         'products':products,
         'quantites':quantity,
         'total':total,
         'all_orders':all_product,
         
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

class OrderView(View):  
    def post(self, request):
        My_orders=[]
        cart=Cart(request)

        all_orders=cart.get_all_info()
        total=cart.get_total_price()

        try:
            order=Order()
            order.order_id=uuid.uuid4()
            order.total_price=total
            order.user_id=request.user
            order.save()
        except:
            raise ValidationError("Order modeliga saqlashdagi hatolik")      
        for item_data in all_orders:
                order_item=OrderItem()
                order_item.order_id=order
                order_item.product_id=item_data['id']
                order_item.price=item_data['price']
                order_item.name=item_data['name']
                order_item.quantity=item_data['quantity']
                order_item.save()    
                data={
                        'item_data':item_data
                    }          
        cart.clear_cart() 
        
        My_orders.append(data)
        asyncio.run(main(f"{My_orders}"))      
        return redirect("product:index")  
    
    
def get_all_orders(request, id):
        cart=Cart(request)
        all_orders=cart.get_all_info()
        orders=OrderItem.objects.all()
        user=get_object_or_404(User, pk=id)
        
        data={
          'orders':  orders,
          'account': user
        }
        
        return render(request, 'product/my_orders.html' , context=data)