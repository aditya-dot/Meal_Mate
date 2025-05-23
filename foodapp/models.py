from django.db import models

class Customer(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 50)
    email = models.CharField(max_length = 35)
    mobile = models.CharField(max_length = 10)
    address = models.CharField(max_length = 100)

class Restaurant(models.Model):
    name = models.CharField(max_length = 50)
    url = models.URLField(max_length = 200,default='https://surl.li/osuzuy')
    cuisine = models.CharField(max_length = 200)
    rating = models.FloatField()

class Menu_Item(models.Model):
    restaurant = models.ForeignKey(Restaurant,on_delete = models.CASCADE, related_name = "items")
    name = models.CharField(max_length = 20)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    vegeterian = models.BooleanField(default=True)
    picture = models.URLField(max_length = 200)

class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete = models.CASCADE,related_name = "cart")
    items = models.ManyToManyField(Menu_Item, related_name = "carts")
    def total_price(self):
        return sum(item.price for item in self.items.all())