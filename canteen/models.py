from django.db import models
from datetime import datetime
#import pytz
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
import math


class Dish(models.Model):
    
    title = models.CharField(max_length=100)
    cooktime = models.IntegerField(default=15)
    price = models.IntegerField(default=0)
    content = models.CharField(max_length=300)
    serving = models.CharField(max_length=100)
    discountPercent = models.IntegerField(default=0)
    onhandqty = models.IntegerField(default=0)
    available = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, default='dish.jpg',  upload_to="images/")

    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dish-detail', kwargs={'pk': self.pk})

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Inventory(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    type = models.CharField(max_length=3)
    qty = models.IntegerField(default=0)
    datetime = models.DateTimeField(default=timezone.now)

class Table(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    available = models.BooleanField(default=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=timezone.now)
    confirmdatetime=models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10)
    cancelled = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    paymentMode=models.CharField(max_length=20, null=True, blank=True)
    isClosed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    @property
    def get_order_total(self):
      orderitems = self.orderdetail_set.all()
      total = sum([item.get_total for item in orderitems])
      return total 

    @property
    def get_order_items_total(self):
      orderitems = self.orderdetail_set.all()
      total = sum([item.quantity for item in orderitems])
      return total

    @property
    def get_order_time_lapsed(self):
      timelapsed = (datetime.now(timezone.utc) - self.confirmdatetime ).seconds
      return timelapsed

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    discountPercent = models.IntegerField(default=0)
     

    @property
    def get_total(self):
        total = math.ceil(self.price * ((100 - self.discountPercent)/100) * self.quantity)
        return total

class Question(models.Model):
    question = models.CharField(max_length=100, null=True, blank=True)
    



class Feedback(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=100, null=True, blank=True)

class Offer(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    discount = models.IntegerField(default=1)
    status = models.CharField(max_length=10)

