from django.db import models
from student.models import User, BaseModel
from django.core.validators import FileExtensionValidator
# Create your models here.
from student.models import User
class Category(BaseModel):
    name=models.CharField(max_length=100)

    def __str__(self) :
        return self.name
    
    class Meta:
        verbose_name='Kategoriya'
        verbose_name_plural='Kategoriyalar'

class Product(BaseModel):
    name=models.CharField(max_length=250)
    users=models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    price=models.PositiveIntegerField(default=0)
    cat=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    about=models.TextField(default='', null=True, blank=True)
    image=models.ImageField(upload_to='product_images/', null=True ,
                            validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])])

    def __str__(self) :
        return self.name

    class Meta:
        verbose_name='Mahsulot'
        verbose_name_plural='Mahsulotlar'

class Order(BaseModel):
    order_id = models.CharField(unique=True, max_length=50)
    order_date = models.DateField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    
    def __str__(self) -> str:
        return self.order_id

class OrderItem(BaseModel):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    quantity = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"{self.name} -- Quantity {self.quantity}"

    @property
    def total_price(self):
        return self.price * self.quantity