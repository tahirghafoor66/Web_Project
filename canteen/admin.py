from django.contrib import admin
from .models import Dish, Table, Order, OrderDetail, Feedback, Offer, Inventory, Question

admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Feedback)
admin.site.register(Offer)
admin.site.register(Inventory)
admin.site.register(Question)
