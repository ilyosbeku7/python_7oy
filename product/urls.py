from django.urls import path
from . import views

app_name='product'

urlpatterns=[
    path('', views.ProductListView.as_view(), name='index'),
    path('category/<int:pk>/', views.CategoryProductList.as_view(), name='category'),
    path('about/<int:id>/', views.About, name='about'),
]