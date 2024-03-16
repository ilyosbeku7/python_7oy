from .models import Product
from django.core.exceptions import ValidationError

class Cart :   

    def get_all_info(self):
        products=self.get_products()
        
        
        result=[]

        for product in products:
            if str(product.id) in self.cart:
                data={
                    'id':str(product.id),
                    'name':str(product.name),
                    'price':str(product.price),
                    'quantity': str(self.cart[str(product.id)])
                }
                result.append(data)
        return  result
    def clear_cart(self):
        self.cart.clear()

        self.session.modified=True
        return True
     

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart=self.session['session_key']={}
        self.cart = cart

   
        
    def add(self, product, quantity):
        product_id = str(product.id)  # Assuming the product has an 'id' attribute
        quantity=int(quantity)
        if quantity <1:
            raise ValueError('Iltimos musbat son kiritin')
        if product_id in self.cart :
            pass
        
        else:
            self.cart[product_id] = str(quantity)
        
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        products_ids=self.cart.keys()

        products=Product.objects.filter(id__in=products_ids)
        return products

    def get_quantity (self):
        quantity=self.cart

        return quantity
    
    def get_total_price(self):
        products_ids=self.cart.keys()
        products=Product.objects.filter(id__in=products_ids)

        total=0

        for key, value in self.cart.items():
            key=int(key)
            for product in products:
                if product.id==key:
                    total=total+(product.price*int(value))
        return total
    
    
    def delete_product(self, product_id):
        product_id=str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified=True

    def product_update(self, product, quantity):
        product_id= str(product.id)
        quantity=int(quantity)
        if quantity>=1:
            self.cart[product_id]=quantity

            self.session.modified=True

            cart=self.cart
            return cart
        else:
           print (ValidationError('Xato raqam kiritildi'))
class Person:
    def __init__(self, name, email) :
        self.email=email
        self.name=name     