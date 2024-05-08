from django.shortcuts import render,redirect
from django.contrib.auth.models import AbstractUser
from .models import *
from . models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.db.models import Max

from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import random
from django.urls import reverse


User = get_user_model()

# Now you can use the User model throughout your code





def index(request):
    return render(request,'index.html')


def contact(request):
    return render(request,'contact.html')


def about(request):
    return render(request,'about.html')


def menu(request):
    menuitems = Item.objects.all()
    burgers = Item.objects.filter(category="Burger")
    b_count = burgers.count()
    pizza = Item.objects.filter(category="Pizza")
    p_count = pizza.count()
    kebab = Item.objects.filter(category="Kebab")
    k_count = kebab.count()
    return render(request, 'menu.html', locals())


def signup(request):
    return render(request,'signup.html')



def User_Signup(request):
    if request.method == 'POST':
        fname = str(request.POST.get('firstname').title())  # title() is for making first letter of name to uppercase
        lname = str(request.POST.get('lastname').title())
        email = request.POST.get('email')
        contact_num = request.POST.get('contact')
        password = request.POST.get('password')
        name= fname + " " + lname

        try:
            User.objects.get(username=email)

            return render(request,'index.html')
        except User.DoesNotExist:
            user= User.objects.create_user(name=name,
                                    first_name=fname,
                                    last_name=lname,
                                    email=email,
                                    phone_number=contact_num,
                                    username=email,
                                    is_superuser=0,
                                    is_staff=0,
                                    user_type=3)

            user.set_password(password)
            user.save()
            login(request, user)
            return redirect(index)
    else:
        return render(request,'signup.html')


def Login_View(request):
    if request.method=='POST':
        email=request.POST.get('username').lower()
        password=request.POST.get('password')
        user=authenticate(email=email,password=password)
        if user is not None:
            if user.is_superuser:
                login(request,user)
                return redirect(admin_dashboard)
            else:
                login(request, user)
                return redirect(index)
        else:
            return render(request,'signup.html')


def Logout_View(request):
    logout(request)
    return redirect(index)


# admin module

def admin_dashboard(request):
    orders = Order.objects.all()
    customer_count = User.objects.filter(user_type=3).count()
    new_orders_count = Order.objects.filter(status=1).count()
    menus_count = Item.objects.all().count()
    
    # Fetch delivered orders and calculate total income
    delivered_orders = Order.objects.filter(status=3)
    total_income = sum(order.total for order in delivered_orders)

    context = {
        'menus_count': menus_count,
        'new_orders_count': new_orders_count,
        'customer_count': customer_count,
        'orders' : orders,
        'total_income': total_income,  # Add total_income to the context
    }
    return render(request, 'admin_dashboard.html', context)

def admin_menu(request):
    menus = Item.objects.all().order_by('-id')
    return render(request, 'admin_menu.html', {'menus': menus})

def user_details(request):
    data = User.objects.filter(is_staff = 0).order_by('-id')
    return render(request,'admin_users.html',locals())

def user_view(request):
    data = User.objects.filter(is_staff = 0).order_by('-id')
    return render(request,'admin_userview.html',locals())

# refer from order_transcript view
def admin_orders(request):               
    data = User.objects.filter(is_staff = 0).order_by('-id')
    user = request.user
    # order_items = Order.objects.filter(user=user)
    # cart_items = Cart.objects.filter(user=user)
    orders = Order.objects.all()
    order_number = request.session.get('order_number', None)

    context = {
        'data': data,
        'orders':orders,
        'order_number': order_number,
        # Add other context data as needed
    }
    return render(request, 'admin_orders.html', context)

# for direct buy orders
def accept_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 2  # Assuming 2 is the status code for 'Pending'
    order.save()

    return redirect('admin_orders')  # Redirect to your admin_orders view after updating status


def cancel_order(request, order_id):
    # Get the order or return a 404 error if it doesn't exist
    order = get_object_or_404(Order, id=order_id)
    
    # Update the order status to 'Cancelled'
    order.status = 0  # Assuming 0 is the status code for 'Cancelled'
    order.save()
    
    return redirect('admin_orders')

def deliver_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.status = 3  # Assuming 3 is the status code for 'Delivered'
    order.save()
    return redirect('admin_orders')  # Redirect to your admin_orders view after updating status


def add_item(request):
    if request.method == 'POST':
        itemcode= request.POST.get('itemcode')
        image = request.FILES.get('image')
        itemname = request.POST.get('name')
        itemdescription = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')

        try:
            data = Item.objects.get(itemcode = itemcode)
            messages.add_message(request, messages.ERROR,
                                 "The item ({}) is already in table".format(data.itemcode)
                                 )
            error = "The item ({}) is already in table".format(data.itemcode)
            return render(request, 'add_item.html',locals())
        except:
            # Create Item
            data = Item.objects.create(itemcode =itemcode,
                                    itemname= itemname,
                                    itemdescription=itemdescription,
                                    image=image,
                                    price=price,
                                    category=category
                                    )
            
            data.save()
            return redirect('admin_menu')
    else:
        return render(request, 'add_item.html')

    


def edit_item(request,item_id):
    menus = Item.objects.filter(id=item_id)
    return render(request,'edit_menu.html',locals())


def edit_menu(request, item_id):
    
    if request.method == 'POST':
        itemcode = request.POST.get('itemcode')
        image = request.FILES.get('image')
        itemname = request.POST.get('name')
        price = request.POST.get('price')
        itemdescription = request.POST.get('description')
        category = request.POST.get('category')
        try:
            data = Item.objects.get(itemcode = itemcode)
            messages.add_message(request, messages.ERROR,
                                 "The itemcode ({}) is already in table".format(data.itemcode)
                                 )
            error = "The item ({}) is already in table".format(data.itemcode)
            return render(request, 'edit_menu.html',locals())
        except:
            Item.objects.filter(id=item_id).update(itemcode=itemcode,
                                                itemname=itemname,
                                                price=price,
                                                itemdescription=itemdescription,
                                                category=category)
            data = get_object_or_404(Item, id=item_id)
            if image:
                data.image= image
            data.save()
            return redirect('admin_menu')
    else:
        return render(request, 'edit_menu.html')
  # Redirect back to edit menu if not POST request

def delete_menu(request, item_id):
    data = get_object_or_404(Item, id=item_id)
    data.delete()  
    return redirect('admin_menu')





# user module

def user_profile(request):
    return render(request,'user_profile.html')

def terms(request):
    return render(request,'terms&cond.html')

def user_contact(request):
    return render(request,'user_contact.html')

def manage_address(request):
    user = request.user
    try:
        address = Address.objects.get(user=user)
        return render(request, 'save_address.html', {'address': address})
    except Address.DoesNotExist:
        return render(request, 'save_address.html') 

def save_address(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        address_text = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        user = request.user

        if not city or not address_text or not zipcode:
            # Fields are empty, redirect with a message
            return redirect('save_address') + '?error=empty_fields'

        # Create or update the address for the current user
        address, created = Address.objects.get_or_create(user=user)
        address.city = city
        address.address = address_text
        address.zip_code = zipcode
        address.save()

        return redirect('manage_address')  # Redirect back to manage_address view
    else:
        return redirect('manage_address')
    

def edit_address(request):
    user = request.user
    try:
        address = Address.objects.get(user=user)
        return render(request, 'update_address.html', {'addres': address})
    except Address.DoesNotExist:
        return render(request, 'update_address.html') 

def update_address(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        address_text = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        user = request.user

        if not city or not address_text or not zipcode:
            # Fields are empty, redirect with a message
            return redirect('edit_address') + '?error=empty_fields'
        # address = Address.objects.get(user=user)
        # address.city = city
        # address.address = address_text
        # address.zip_code = zipcode
        
        Address.objects.filter(user=user).update(city = city,address = address_text,zip_code = zipcode
                                        )
        
        return redirect('manage_address')            # Redirect back to manage_address view
    else:
        return redirect('edit_address')            # Redirect back to manage_address view
    # return render(request, 'edit_address.html') 






# Add to cart
# from menu-cart-checkout_all.html
# @login_required
def cart(request):
    user = request.user
    cart_items = Cart.objects.filter(user=user)
    
    # Calculate cart_total for each item
    for item in cart_items:
        item.cart_total = item.quantity * item.item.price
        item.save()

    # Recalculate grand_total after updating cart_total
    grand_total = sum(item.cart_total for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'grand_total': grand_total})

# @login_required
def add_to_cart(request, item_id):
    user = request.user
    item = Item.objects.get(id=item_id)
    try:
        cart_item = Cart.objects.get(user=user, item=item)
        cart_item.quantity += 1
        cart_item.save()
    except Cart.DoesNotExist:
        Cart.objects.create(user=user, item=item, quantity=1)
    return redirect('cart')

def decrement_quantity(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = Cart.objects.get(id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.cart_total = cart_item.quantity * cart_item.item.price  # Update total based on decreased quantity
                cart_item.save()
        except Cart.DoesNotExist:
            pass
    return redirect('cart')

def increment_quantity(request, cart_item_id):
    if request.method == 'POST':
        try:
            cart_item = Cart.objects.get(id=cart_item_id)
            cart_item.quantity += 1
            cart_item.cart_total = cart_item.quantity * cart_item.item.price  # Update total based on increased quantity
            cart_item.save()
        except Cart.DoesNotExist:
            pass
    return redirect('cart')

def remove_from_cart(request, item_id):
    try:
        cart_item = Cart.objects.get(id=item_id)
        cart_item.delete()
    except Cart.DoesNotExist:
        pass  # Handle the case where the item is not found in the cart

    return redirect('cart')  # Redirect to the cart page after removal

def checkout_all(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    items = Item.objects.all()
    grand_total = sum(item.cart_total for item in cart)
    address = Address.objects.get(user=user)


    return render(request,'checkout_all.html',locals())


def add_to_checkout(request, item_id):
    items = get_object_or_404(Item, id=item_id)
    
    # Convert Decimal to float for serialization
    item_price = float(items.price)
    
    # Store item details in the session
    request.session['checkout_item'] = {
        'item_id': items.id,
        'item_image': items.image.url if items.image else '',  # Store the image URL
        'item_name': items.itemname,
        'item_description': items.itemdescription,
        'item_price': item_price,  # Use the converted float value
    }
    
    messages.success(request, f"{items.itemname} added to checkout.")
    return redirect('checkout')


def checkout(request):
    user = request.user
    address = Address.objects.get(user=user)

    # Retrieve item details from session
    item_details = request.session.get('checkout_item')
    print(item_details)  # Debugging line

    # Check if item_details exist in session
    if item_details:
        item_id = item_details['item_id']
        item_image = item_details['item_image']

        item_name = item_details['item_name']
        item_description = item_details['item_description']
        item_price = Decimal(item_details['item_price'])  # Convert back to Decimal

        # Get quantity from the form data
        quantity = int(request.POST.get('quantity', 1))

        # Calculate total price based on quantity
        total_price = item_price * quantity

        context = {
            'item_image': item_image,
            'item_id': item_id,
            'item_name': item_name,
            'item_price': item_price,
            'item_description': item_description,
            'quantity': quantity,
            'total_price': total_price,
            'address':address, # Add total price to the context
        }
        return render(request, 'checkout.html', context)
    else:
        # Handle case where item_details are not found
        return redirect('menu')


    
def remove_from_order(request, item_id):
    try:
        order_item = Item.objects.get(id=item_id)
        order_item.delete()
    except Order.DoesNotExist:
        pass  # Handle the case where the item is not found in the cart

    return redirect('checkout')  # Redirect to the cart page after removal

def order_transcript(request):
    if request.method == 'POST':
        # Check if the request is coming from the checkout page
        if request.POST.get('from_checkout') == 'true':
            # Process the order since it's from the checkout page
            item_id = request.POST.get('item_id')
            item_name = request.POST.get('item_name')
            item_price = request.POST.get('item_price')
            quantity = request.POST.get('quantity')
            user_id = request.user.id
            item_id = request.POST.get('item_id')
            item = Item.objects.get(id=item_id)  # Assuming you have an Item model
            item_image = item.image.url

            # Calculate total based on item price and quantity
            total = float(item_price) * int(quantity)
            if 'order_number' not in request.session:
                order_number = random.randint(100000, 999999)
                request.session['order_number'] = order_number
            else:
                order_number = request.session['order_number']

            # Create a new Order instance and save it
            order = Order.objects.create(
                user_id=user_id,
                item_id=item_id,
                quantity=quantity,
                total=total,
            )

            # Pass the item details to the template
            context = {
                'order_number': order_number,  # Assuming order_number is generated during order creation
                'item_name': item_name,
                'item_price': item_price,
                'quantity': quantity,
                'total': total,
                'item_image': item_image,

            }

            # Render the order transcript page with the item details
            return render(request, 'order_transcript.html', context)

    # Render the order transcript page without item details if not from checkout page
    return render(request, 'order_transcript.html')



def order_transcript_cart(request):
    user = request.user

    # Get the user's cart items
    cart_items = Cart.objects.filter(user=user)

    # Calculate the total price for the latest order
    total = sum(item.quantity * item.item.price for item in cart_items)
    total_float = float(total)

    # Save the total in the session
    request.session['total'] = total_float
    request.session.save()

    # Generate an order number if it doesn't exist in the session
    order_number = request.session.get('order_number')
    if not order_number:
        order_number = random.randint(100000, 999999)
        request.session['order_number'] = order_number

    # Check if there are items in the cart
    if cart_items.exists():
        for cart_item in cart_items:
            # Create a new order for each item in the cart
            Order.objects.create(
                user=user,
                item=cart_item.item,
                status=1,  # Assuming 'New' status for new orders
                total=total,
                quantity=cart_item.quantity
            )

        # Clear the cart after processing orders
        cart_items.delete()

    # Get the timestamp of the latest order for this user
    latest_order_timestamp = Order.objects.filter(user=user).aggregate(Max('created_at'))['created_at__max']

    # Fetch the latest order items for the user, excluding the latest order
    latest_order_items = Order.objects.filter(user=user, created_at=latest_order_timestamp).order_by('-created_at')[:5]

    # Redirect to the order transcript page with the latest order items
    return render(request, 'order_transcript_cart.html', {'order_items': latest_order_items, 'total': total_float, 'order_number': order_number})


# def order_transcript(request, order_id):
#     # Fetch the order based on the order_id
#     order = get_object_or_404(Order, id=order_id)
    
#     # Fetch order items associated with the order
#     order_items = OrderItem.objects.filter(order=order)

#     # Render the order_transcript.html template with order details
#     return render(request, 'order_transcript.html', {
#         'order': order,
#         'order_items': order_items,
#     })


# def checkout(request):
#     user = request.user
#     order_items = Order.objects.filter(user=user)
#     total = sum(item.quantity * item.item.price for item in order_items)
#     address = Address.objects.get(user=user)

# def decrement_order_quantity(request, item_id):
#     if request.method == 'POST':

#         order_item = get_object_or_404(Item, id=item_id)
#         if order_item.quantity > 1:
#             order_item.quantity -= 1
#             order_item.save()
    
#     return redirect('checkout')  # Redirect to the checkout page after decrementing

# def increment_order_quantity(request, item_id):
#     if request.method == 'POST':
#         order_item = get_object_or_404(Item, id=item_id)
#         order_item.quantity += 1
#         order_item.save()
#     return redirect('checkout')  # Redirect to the checkout page after incrementing

# def increment_order_quantity(request, item_id):
#     order_item = get_object_or_404(Item, pk=item_id)
#     order_item.quantity += 1
#     order_item.save()
#     return redirect('checkout')


# def order_transcript(request):
#     user = request.user

#     # Assuming you have models for Order, Address, and PaymentMethod
#     order_items = Order.objects.filter(user=user)
#     address = Address.objects.get(user=user)
    
#     order_number = random.randint(100000, 999999)
#     total_price = sum(item.quantity * item.item.price for item in order_items)

#      # Check if order number exists in session, otherwise generate and store
#     if 'order_number' not in request.session:
#         order_number = random.randint(100000, 999999)
#         request.session['order_number'] = order_number
#     else:
#         order_number = request.session['order_number']
        
#     new_order = Order.objects.create(user=user, status=0)
#     new_order.save()

#     return render(request, 'order_transcript.html', {
#         'order_items': order_items,
#         'address': address,
#         'order_number': order_number,
#         'total_price': total_price,
#     })










# def checkout_items(request,item_id):
#     user = request.user
#     item = Item.objects.get(id=item_id)
#     try:
#         data = Cart.objects.get(item=item_id)
#         quantity = data.quantity + 1
#         Cart.objects.filter(item=item_id).update(quantity=quantity)
#         return redirect(menu)
#     except:
#         data = Cart.objects.create(user=user,
#                                 item=item,
#                                 quantity=1
#                                 )
#         data.save()

#         return redirect(order)
    
# def adjust_quantity(request, item_id):
#     cart_item = get_object_or_404(Cart, user=request.user, item_id=item_id)
#     if request.method == 'POST':
#         action = request.POST.get('action')
#         if action == 'add':
#             cart_item.quantity += 1
#         elif action == 'minus':
#             cart_item.quantity = max(cart_item.quantity - 1, 0)
#         # Update cart total based on item price and quantity
#         item = get_object_or_404(Item, id=item_id)
#         cart_item.cart_total = item.price * cart_item.quantity
#         cart_item.save()
#         return redirect(checkout, item_id=item_id)
#     return HttpResponseBadRequest('Invalid request')


        

# def adjust_quantity(request, item_id):
#     if request.method == 'POST':
#         quantity_adjustment = int(request.POST.get('quantity_adjustment', 0))
#         if quantity_adjustment == 0:
#             return HttpResponseBadRequest('Invalid quantity adjustment value')

#         try:
#             cart_item = Cart.objects.get(item_id=item_id, user=request.user)
#             new_quantity = cart_item.quantity + quantity_adjustment

#             # Ensure quantity doesn't go below 1
#             new_quantity = max(new_quantity, 1)

#             cart_item.quantity = new_quantity

#             # Get the item price and update the total price in the cart item
#             item = Item.objects.get(id=item_id)
#             cart_item.cart_total = item.price * new_quantity

#             cart_item.save()
#         except Cart.DoesNotExist:
#             return HttpResponseBadRequest('Item not found in cart')
#         except Item.DoesNotExist:
#             return HttpResponseBadRequest('Item not found')

#     return redirect(checkout, item_id=item_id)


# def cart_adjustment(request, item_id):
#     if request.method == 'POST':
#         quantity_adjustment = int(request.POST.get('quantity_adjustment', 0))
#         if quantity_adjustment == 0:
#             # Invalid quantity adjustment value
#             return HttpResponseBadRequest('Invalid quantity adjustment value')

#         try:
#             cart_item = Cart.objects.get(item_id=item_id, user=request.user)
#             new_quantity = cart_item.quantity + quantity_adjustment
#             if new_quantity < 1:
#                 # Ensure quantity doesn't go below 1
#                 new_quantity = 1

#             cart_item.quantity = new_quantity

#             # Get the item price and update the total price in the cart item
#             item = Item.objects.get(id=item_id)
#             cart_item.total = item.price * new_quantity

#             cart_item.save()
#         except Cart.DoesNotExist:
#             # Handle case where item is not in cart
#             return HttpResponseBadRequest('Item not found in cart')
#         except Item.DoesNotExist:
#             # Handle case where item does not exist
#             return HttpResponseBadRequest('Item not found')

#     return redirect('checkout')


# def increment_quantity(request, item_id):
#     if request.method == 'POST':
#         try:
#             cart_item = Cart.objects.get(item_id=item_id, user=request.user)
#             new_quantity = cart_item.quantity + 1
#             cart_item.quantity = new_quantity

#             # Get the item price and update the total price in the cart item
#             item = Item.objects.get(id=item_id)
#             cart_item.total_price = item.price * new_quantity

#             cart_item.save()
#         except Cart.DoesNotExist:
#             # Handle case where item is not in cart
#             return HttpResponseBadRequest('Item not found in cart')
#         except Item.DoesNotExist:
#             # Handle case where item does not exist
#             return HttpResponseBadRequest('Item not found')

#     return redirect('checkout')


# def decrement_quantity(request, item_id):
#     if request.method == 'POST':
#         try:
#             cart_item = Cart.objects.get(item_id=item_id, user=request.user)
#             new_quantity = max(cart_item.quantity - 1, 1)  # Ensure quantity doesn't go below 1
#             cart_item.quantity = new_quantity

#             # Get the item price and update the total price in the cart item
#             item = Item.objects.get(id=item_id)
#             cart_item.total_price = item.price * new_quantity

#             cart_item.save()
#         except Cart.DoesNotExist:
#             # Handle case where item is not in cart
#             return HttpResponseBadRequest('Item not found in cart')
#         except Item.DoesNotExist:
#             # Handle case where item does not exist
#             return HttpResponseBadRequest('Item not found')

#     return redirect('checkout')     













