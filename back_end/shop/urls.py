from django.urls import path

from . import views

urlpatterns = [
    path('item/', views.get_all_item, name='get_all_item'),
    path('item/<int:item_id>/', views.get_item_info, name='get_item_info'),
    path('item_type/', views.get_item_type, name='get_all_item'),
    path('item_type/<int:type_id>/', views.get_item_from_type, name='get_item_from_type'),
    path('cart/', views.cart, name='get_cart'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('order/', views.get_order, name='get_order'),
    path('login/', views.login, name='login'),
]
