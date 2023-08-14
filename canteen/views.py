import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from .views import *
from .models import *
from .utils import * 
from .forms import FeedbackForm
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)



def home(request):
    if request.user.is_authenticated:
        groupid=getGroupId(request.user)
    else:
        groupid = 0
        
    
    context = {"groupid": groupid}
    return render(request, 'canteen/home.html',context)


class DishListView(LoginRequiredMixin, ListView):
    model = Dish
    template_name = 'canteen/menu.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'dishes'
    ordering = ['title']


class DishDetailView(LoginRequiredMixin, DetailView):
    model = Dish


class DishCreateView(LoginRequiredMixin, CreateView):
    model = Dish
    success_url = '/menu/'
    fields = [ 'title', 'price', 'content','serving','available', 'image']

    def test_func(self):
        if self.request.user == 'Admin':
            return True
        return False

    
class DishUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Dish
    success_url = '/menu/'
    fields = [ 'title', 'price', 'content', 'serving', 'onhandqty', 'discountPercent', 'available','image']

    def form_valid(self, form):
        #form.instance.chef = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False

class DishDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Dish
    success_url = '/menu/'

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


@login_required
def custOrder(request):
    if request.user.is_authenticated:
        customer=request.user
        user=request.user
        try:
            order=Order.objects.get(customer=customer, isClosed=False)
        except Order.DoesNotExist:
            table=getTable()
            
            order=Order(customer=customer, isClosed=False, table=table, status='New')
            dt = order.datetime
            #print(dt.strftime("%Y%m%d%H%M%S")+str(user.id))
            order.transaction_id=dt.strftime("%Y%m%d%H%M%S")+str(user.id)
            order.save()
        
        items = order.orderdetail_set.all()
    else:
        order = None
        items = None

    context = {'items':items, 'order':order,  'user': user}
    return render(request, 'canteen/order.html', context)


@login_required
def viewOrder(request, id):
    if request.user.is_authenticated:
        user=request.user
        try:
            order=Order.objects.get(id=id)
            items = order.orderdetail_set.all()
        except Order.DoesNotExist:
            order=None
            items=None
    else:
        order = None
        items = None

    context = {'items':items, 'order':order,  'user': user}
    return render(request, 'canteen/vieworder.html', context)

@login_required
def pendingOrders(request):
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            orders=Order.objects.filter(status='Confirmed')
            if not orders:
                print('no pending order found')
                message = 'No Pending Orders Found'
                orderdetails = None                

            else:
                print('Pending Orders Found')
                print(orders)
                """ for o in orders:
                    print(o.id)
                    items=o.orderdetail_set.all()
                    print(items) """
                #print('order object')
                #print(items)
                message = 'Following Orders are Pending'
                orderdetails=OrderDetail.objects.filter(order__in=orders)
                print('order details .....')
                print(orderdetails)
        except Order.DoesNotExist:
            orders = None
            orderdetails = None
            message = 'No Pending Order Found'
    else:
        orders = None
        orderdetails = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'orders':orders, 'orderdetails':orderdetails, 'user': user, 'message': message}
    return render(request, 'canteen/pendingorders.html', context)


@login_required
def viewSales(request, scope):
    date=datetime.now()
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            year=date.strftime("%Y")
            month=date.strftime("%m")
            day=date.strftime("%d")
            
            if scope == 'Year':
                scopeMsg=year
                orders=Order.objects.filter(datetime__year=year)
            elif scope == 'Month':
                scopeMsg=month
                orders=Order.objects.filter(datetime__month=month , datetime__year=year)
            elif scope == 'Day':
                scopeMsg=day
                orders=Order.objects.filter(datetime__day=day , datetime__month=month , datetime__year=year)

            ordersCount=orders.count()
            if  ordersCount > 0 :
                totalSale=sum([ order.get_order_total for order in orders])
                totalItems=sum([ order.get_order_items_total for order in orders])
                message = 'Sales Data for the ' + scope + ' ' + scopeMsg 
            else:
                totalSale=0
                totalItems=0
                message = 'No Sales Data found for the ' + scope + ' ' + scopeMsg

        except Order.DoesNotExist:
            ordersCount=0
            totalSale=0
            totalItems=0
            orders = None
            message = 'Sales Data not found for the ' + scope   
    else:
        ordersCount=0
        totalSale=0
        totalItems=0
        orders = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'orders':orders, 'user': user, 'message': message, 'date': date, 
                'ordersCount': ordersCount,'totalSale':  format(totalSale, ","), 'totalItems':totalItems }
    return render(request, 'canteen/viewsales.html', context)


@login_required
def dishSales(request):
    dishSelected=0
    if request.method == 'POST':
        print(request.POST.get)
        dishSelected=request.POST.get('dish',0)

    date=datetime.now()
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            if dishSelected == 0:
                print('id is 0')
                dishesOrdered=OrderDetail.objects.all()
                scopeMsg='All Dishes'
            else:
                dish=Dish.objects.get(id=dishSelected)
                scopeMsg=dish.title
                dishesOrdered=OrderDetail.objects.filter(dish=dish)
            
            dishesOrderedCount=dishesOrdered.count()
            if  dishesOrderedCount > 0 :
                totalSale=sum([ dish.get_total for dish in dishesOrdered])
                totalItems=sum([ dish.quantity for dish in dishesOrdered])
                message = 'Sales Data for ' +  scopeMsg 
            else:
                totalSale=0
                totalItems=0
                message = 'No Sales Data found for ' +  scopeMsg

            dishes=Dish.objects.all()
        except OrderDetail.DoesNotExist:
            dishesOrderedCount=0
            dishes = None
            totalSale=0
            totalItems=0
            dishesOrdered = None
            message = 'Sales Data not found for the ' + scopeMsg   
    else:
        dishesOrderedCount=0
        dishes=None
        totalSale=0
        totalItems=0
        dishesOrdered = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'dishesOrdered':dishesOrdered, 'user': user, 'message': message, 'date': date, 
                'dishesOrderedCount': dishesOrderedCount,'totalSale':  format(totalSale, ","), 'totalItems':totalItems, 'dishes':dishes }
    return render(request, 'canteen/dishsales.html', context)


@login_required
def changeOrders(request):
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            orders=Order.objects.filter(status='Edit Requested') | Order.objects.filter(status='Cancel Requested') 
            if not orders:
                print('No change order requests found')
                message = 'No change order requests found'
                orderdetails = None                

            else:
                print('Pending Change Orders Requests Found')
                print(orders)
                """ for o in orders:
                    print(o.id)
                    items=o.orderdetail_set.all()
                    print(items) """
                #print('order object')
                #print(items)
                message = 'Pending Change Orders Requests Found'
                orderdetails=OrderDetail.objects.filter(order__in=orders)
                print('order details .....')
                print(orderdetails)
        except Order.DoesNotExist:
            orders = None
            orderdetails = None
            message = 'No change order requests found'
    else:
        orders = None
        orderdetails = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'orders':orders, 'orderdetails':orderdetails, 'user': user, 'message': message}
    return render(request, 'canteen/changeorders.html', context)


@login_required
def unpaidOrders(request):
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            orders=Order.objects.filter(paid=False, cancelled=False)
            if not orders:
                message = 'No Unpaid Orders Found'
                orderdetails = None                

            else:
                message = 'Following Orders are Unpaid'
                
        except Order.DoesNotExist:
            orders = None
            message = 'No Unpaid Order Found'
    else:
        orders = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'orders':orders, 'user': user, 'message': message}
    return render(request, 'canteen/unpaidorders.html', context)


@login_required
def Tables(request):
    if request.user.is_authenticated:
        user=request.user
        groupid=getGroupId(user)
        try:
            tables=Table.objects.all()
            message = 'Tables Detail'
        except Table.DoesNotExist:
            tables = None
            message = 'No Tables Found'
    else:
        tables = None
        user = None
        message = None
        groupid=0

    context = {'groupid':groupid, 'tables':tables, 'user': user, 'message': message}
    return render(request, 'canteen/tables.html', context)


@login_required
def confirmOrder(request, id):
    user=request.user
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        confirm=True
        items = order.orderdetail_set.all()
        for item in items:
            if item.quantity > item.dish.onhandqty and confirm:
                confirm=False
            

        
        if confirm:
            for item in items:
                item.dish.onhandqty -= item.quantity
                if item.dish.onhandqty == 0 :
                    item.dish.available = False
                item.dish.save()
            
            order.status='Confirmed'
            order.confirmdatetime=timezone.now()
            order.save()
            message="Order has been confirmed"
        else:
            message="Ordered Quantaties are not available"    
    else:
        order = None

    context = {'items':items, 'order':order,  'user': user, 'message': message}
    return render(request, 'canteen/order.html', context)

    


@login_required
def requestBill(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        order.status='Bill Requested'
        order.save()    
    else:
        order = None

    return HttpResponseRedirect('/order')


@login_required
def paymentMade(request, id):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.get(id=id)
        order.status='Payment Made'
        order.paymentMode=request.POST.get('option', 'No payment mode selected')
        order.save()    
    else:
        order = None
        user = None

    context = {'order':order,  'user': user}    
    return render(request, 'canteen/thanks.html', context)

@login_required
def billPaid(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        order.status='Bill Paid'
        order.paid=True
        order.save()    
    else:
        order = None

    return HttpResponseRedirect('/unpaidorders')
                            
    

@login_required
def makePayment(request, id):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.get(id=id)
    else:
        order = None
    context = {'order':order,  'user': user}
    return render(request, 'canteen/makepayment.html', context)



@login_required
def cookOrder(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        order.status='Cooked'
        order.save()    
    else:
        order = None
    return HttpResponseRedirect('/pendingorders')


@login_required
def allowChange(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        items = order.orderdetail_set.all()
        for item in items:
            item.dish.onhandqty += item.quantity
            item.dish.available=True
            item.dish.save()

        if order.status == 'Edit Requested':
            order.status='Open'
        elif order.status == 'Cancel Requested':
            order.status = 'Canceled'
            order.cancelled = True
        
        order.save()    
    else:
        order = None
    return HttpResponseRedirect('/changeorders')


@login_required
def feedback(request, id):
    if request.user.is_authenticated:
        user=request.user
        order=Order.objects.get(id=id)
        if request.method == 'POST':
            feedbacks=Feedback.objects.filter(order=order)
            for feedback in feedbacks:
                feedback.answer = request.POST.get(f'{feedback.id}', 'No Answer')
                feedback.save()
            
            order.status='Feedback Given'
            order.isClosed=True
            order.save()
            order.table.available=True
            order.table.save()
            return HttpResponseRedirect('/')
        else:
            questions=Question.objects.all()
            feedbacks=loadFeedback(order,questions)        
            
    else:
        order = None
        user = None
        feedbacks = None

    context = {'order':order,  'user': user, 'feedbacks': feedbacks}
    return render(request, 'canteen/feedback.html', context)


@login_required
def cancelOrder(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        order.status='Cancel Requested'
        order.save()    
    else:
        order = None

    return HttpResponseRedirect('/order')

@login_required
def editOrder(request, id):
    if request.user.is_authenticated:
        order=Order.objects.get(id=id)
        order.status='Edit Requested'
        order.save()    
    else:
        order = None

    return HttpResponseRedirect('/order')


def addOrderItem(request, id):
    if request.method == 'POST':
        customer=request.user
        user=request.user
        try:
            order=Order.objects.get(customer=customer, isClosed=False)
            if order.status == 'New':
                order.status ='Open'
                order.save()

        except Order.DoesNotExist:
            table=getTable()
            order=Order(customer=customer, isClosed=False, table=table, status='Open')
            dt = order.datetime
            order.transaction_id=dt.strftime("%Y%m%d%H%M%S")+str(user.id)
            order.save()

        if order.status == 'Open':
            dish = Dish.objects.get(pk=id)
            orderitem, created = OrderDetail.objects.get_or_create(order=order, dish=dish)
            if orderitem.quantity == 0 :
              orderitem.quantity += 1
              orderitem.price = dish.price
              orderitem.discountPercent = dish.discountPercent
              orderitem.save()
              message=dish.title + " has been added to the Order"
            else:
                message=dish.title + " is already added in the Order, please change Quantity"
        else:
            message="Item can be added only when order status is Open"
            
        items = order.orderdetail_set.all()
        
        context = {'items':items, 'order':order,  'user': user, 'message': message}
        return render(request, 'canteen/order.html', context)

def moreOrderItem(request, id):
    if request.method == 'POST':
        rec = OrderDetail.objects.get(pk=id)
        rec.quantity = (rec.quantity + 1)
        rec.save()
        return HttpResponseRedirect('/order')

def lessOrderItem(request, id):
    if request.method == 'POST':
        rec = OrderDetail.objects.get(pk=id)
        rec.quantity = (rec.quantity - 1)
        rec.save()
        if rec.quantity == 0 :
            rec.delete()
        return HttpResponseRedirect('/order')

def delOrderItem(request, id):
    if request.method == 'POST':
        rec = OrderDetail.objects.get(pk=id)
        rec.delete()
        return HttpResponseRedirect('/order')
