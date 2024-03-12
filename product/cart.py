

class Cart :   
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key', {})
        self.cart = cart

    def add(self, product):
        product_id = str(product.id)  # Assuming the product has an 'id' attribute
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = str(product.price)
        self.session['session_key'] = self.cart
        self.session.modified = True

    def __len__(self):
        return len(self.cart)

class Person:
    def __init__(self, name, email) :
        self.email=email
        self.name=name     