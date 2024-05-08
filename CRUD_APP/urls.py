from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('menu/', views.menu, name='menu'),
    path('contact/', views.contact, name='contact'),
    # path('order/', views.order, name='order'),
    path('cart/', views.cart, name='cart'),
    path('signup/', views.signup, name='signup_page'),
    path('User_Signup/', views.User_Signup, name='signup'),
    path('Logout/', views.Logout_View, name='logout'),
    path('Login/', views.Login_View, name='login'),



    # admin

    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_menu/', views.admin_menu, name='admin_menu'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('deliver_order/<int:order_id>/', views.deliver_order, name='deliver_order'),
   



    path('add_item/', views.add_item, name='add_item'),
    
    path('edit_item/<int:item_id>/', views.edit_item, name='edit_item'),
    path('edit_menu/<int:item_id>/', views.edit_menu, name='edit_menu'),

    path('delete_menu/<int:item_id>/', views.delete_menu, name='delete_menu'),

    path('user_details/', views.user_details, name='user_details'),
    path('user_view/', views.user_view, name='user_view'),


     # user

    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrement_quantity/<int:cart_item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('increment_quantity/<int:cart_item_id>/', views.increment_quantity, name='increment_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout_all/', views.checkout_all, name='checkout_all'),

    path('add_to_checkout/<int:item_id>/', views.add_to_checkout, name='add_to_checkout'),
    path('checkout/', views.checkout, name='checkout'),
    # path('decrement_order_quantity/<int:item_id>/', views.decrement_order_quantity, name='decrement_order_quantity'),
    # path('increment_order_quantity/<int:item_id>/', views.increment_order_quantity, name='increment_order_quantity'),
    path('remove_from_order/<int:item_id>/', views.remove_from_order, name='remove_from_order'),


    # final order transcript 
    path('order_transcript/', views.order_transcript, name='order_transcript'),

    # path('order_transcript/', views.order_transcript, name='order_transcript'),
    path('order_transcript_cart/', views.order_transcript_cart, name='order_transcript_cart'),




    path('user_profile/', views.user_profile, name='user_profile'),
    path('terms/', views.terms, name='terms'),
    path('user_contact/', views.user_contact, name='user_contact'),

    path('manage_address/', views.manage_address, name='manage_address'),
    path('save_address/', views.save_address, name='save_address'),

    path('edit_address/', views.edit_address, name='edit_address'),
    path('update_address/', views.update_address, name='update_address'),


    # path('checkout_items/<int:item_id>/', views.checkout, name='checkout_items'),

    # path('adjust_quantity/<int:item_id>/', views.adjust_quantity, name='adjust_quantity'),







]
