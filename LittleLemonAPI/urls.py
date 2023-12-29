from django.urls import path
from .views import return_user, get_managers, remove_manager, \
    get_delivery_crew, remove_delivery_crew, get_post_menu_items, edit_single_menu_item, \
    edit_cart, manage_orders, manage_specific_order

urlpatterns = [
    path('users/users/me/', return_user),
    path('groups/manager/users', get_managers),
    path('groups/manager/users/<int:userId>/', remove_manager),
    path('groups/delivery-crew/users', get_delivery_crew),
    path('groups/delivery-crew/users/<int:userId>/', remove_delivery_crew),
    path('menu-items/', get_post_menu_items),
    path('menu-items/<menu_item>/', edit_single_menu_item),
    path('cart/menu-items/', edit_cart),
    path('orders/', manage_orders),
    path('orders/<int:orderId>/', manage_specific_order)
]