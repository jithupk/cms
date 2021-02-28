from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product'),
    path('customer/<str:pk>/', views.customer, name='customer'),
    path('create_order/<str:pk>/', views.CreateOrder, name='create_order'),
    path('update/<str:pk>/', views.OrderUpdate, name='order_update'),
    path('delete/<str:pk>/', views.OrderDelete, name='order_delete'),
    path('login/',views.login, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('register/', views.register, name='register'),
    path('settings/', views.accountSettings, name='settings')
]
