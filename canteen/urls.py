from django.urls import path
from .views import (
    DishListView,
    DishDetailView,
    DishCreateView,
    DishUpdateView,
    DishDeleteView
)
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.home, name='canteen-home'),
    path('menu/', DishListView.as_view(), name='canteen-menu'),
    path('dish/new/', DishCreateView.as_view(), name='dish-create'),
    path('dish/<int:pk>/', DishDetailView.as_view(), name='dish-detail'),
    path('dish/<int:pk>/update/', DishUpdateView.as_view(), name='dish-update'),
    path('dish/<int:pk>/delete/', DishDeleteView.as_view(), name='dish-delete'),
    path('viewsales/<str:scope>', views.viewSales, name='canteen-sales'),
    path('dishsale/', views.dishSales, name='dishsales'),
    path('order/', views.custOrder, name='canteen-order'),
    path('vieworder/<int:id>', views.viewOrder, name='vieworder'),
    path('pendingorders/', views.pendingOrders, name='pending-orders'),
    path('changeorders/', views.changeOrders, name='change-orders'),
    path('cookorder/<int:id>', views.cookOrder, name='cookorder'),
    path('billpaid/<int:id>', views.billPaid, name='billpaid'),
    path('allowchange//<int:id>', views.allowChange, name='allowchange'),
    path('unpaidorders/', views.unpaidOrders, name='unpaid-orders'),
    path('tables/', views.Tables, name='tables'),
    path('confirmorder/<int:id>', views.confirmOrder, name='confrimorder'),
    path('requestbill/<int:id>', views.requestBill, name='requestbill'),
    path('makepayment/<int:id>', views.makePayment, name='makepayment'),
    path('paymentmade/<int:id>', views.paymentMade, name='paymentmade'),
    path('feedback/<int:id>', views.feedback, name='feedback'),
    path('cancelorder/<int:id>', views.cancelOrder, name='cancelorder'),
    path('editorder/<int:id>', views.editOrder, name='editorder'),
    path('add/<int:id>/', views.addOrderItem, name="addorderitem"),
    path('delete/<int:id>/', views.delOrderItem, name="delorderitem"),
    path('more/<int:id>/', views.moreOrderItem, name="moreorderitem"),
    path('less/<int:id>/', views.lessOrderItem, name="lessorderitem"),
   ]

