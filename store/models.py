from distutils.command.upload import upload
from io import BytesIO
from unicodedata import category
from PIL import Image

from django.core.files import File
from django.db import models

# Create your models here.

class Collection(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('name',)
    
    def __str__(self):
        return self.name

    def absolute_url(self):
        return f'/{self.slug}'

class Product(models.Model):
    collection = models.ForeignKey(Collection, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    stock_unit = models.CharField(max_length=255, unique=True)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    # total_inventory = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    # total_revenue = models.DecimalField(max_digits=12, decimal_places=0, default=0)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def absolute_url(self):
        return f'/{self.collection.slug}/{self.slug}'

    def product_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
    def product_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    # def calculate_total_inventory(self):
    #     self.total_inventory = self.inventory*self.purchase_price


# TODO: Create an order model.
#           - Order and orderItem: One to many relationship.
#           - Fields: created at, and list of orderItems.
# TODO: Create an orderItem model.
#           - OrderItem and product: many to one relationship.
#           - Fields: product details and quantity
# TODO: Create a cart model.
#           - cart and cartItem: one to many relationship.
#           - Fields: created_at and list of cartItems.
# TODO: Create a cartItem model.
#           - cartItem and product: many to one relationship.
#           - Fields: product details and quantity.
# class Order(models.Model):
#     product = models.ForeignKey(Product, related_name='cartItems')








    

