from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import get_object_or_404
# Create your views here.
# def index(request):
#     return render( request, 'product/index.html')


class ProductListView(ListView):
    model=Product
    template_name='product/index.html'
    context_object_name='products'

    extra_context={
        'categories':Category.objects.all()
    }
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