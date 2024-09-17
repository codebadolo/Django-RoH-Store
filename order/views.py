from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.crypto import get_random_string

from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from product.models import Category, Product, Variants
from user.models import UserProfile


def index(request):
    return HttpResponse("Order Page")


@login_required(login_url='/login')  # Check login
def addtoshopcart(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    product = Product.objects.get(pk=id)

    if product.variant != 'None':
        variantid = request.POST.get('variantid')  # from variant add to cart
        checkinvariant = ShopCart.objects.filter(variant_id=variantid, user_id=current_user.id)  # Check product in shopcart
        control = 1 if checkinvariant else 0  # Product in cart or not
    else:
        checkinproduct = ShopCart.objects.filter(product_id=id, user_id=current_user.id)  # Check product in shopcart
        control = 1 if checkinproduct else 0

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control == 1:  # Update shopcart
                data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:  # Insert into Shopcart
                data = ShopCart(user_id=current_user.id, product_id=id, variant_id=variantid, quantity=form.cleaned_data['quantity'])
                data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)

    else:  # if there is no post
        if control == 1:  # Update shopcart
            data = ShopCart.objects.get(product_id=id, user_id=current_user.id)
            data.quantity += 1
            data.save()
        else:  # Insert into Shopcart
            data = ShopCart(user_id=current_user.id, product_id=id, quantity=1, variant_id=None)
            data.save()
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)


@login_required(login_url='/login')
def shopcart(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum([item.product.price * item.quantity for item in shopcart])
    context = {
        'shopcart': shopcart,
        'category': Category.objects.all(),
        'total': total,
    }
    return render(request, 'shopcart_products.html', context)


@login_required(login_url='/login')  # Check login
def deletefromcart(request, id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item was deleted from Shopcart.")
    return HttpResponseRedirect("/shopcart")


@login_required(login_url='/login')  # Check login
def orderproduct(request):
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total = sum([item.variant.price * item.quantity if item.variant else item.product.price * item.quantity for item in shopcart])

    if request.method == 'POST':  # if there is a post
        form = OrderForm(request.POST)
        if form.is_valid():
            # Save order
            order = Order(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                phone=form.cleaned_data['phone'],
                user_id=current_user.id,
                total=total,
                ip=request.META.get('REMOTE_ADDR'),
                code=get_random_string(5).upper()
            )
            order.save()

            # Save order products
            for item in shopcart:
                order_product = OrderProduct(
                    order=order,
                    product=item.product,
                    user=current_user,
                    quantity=item.quantity,
                    price=item.variant.price if item.variant else item.product.price,
                    amount=item.amount,
                    variant=item.variant
                )
                order_product.save()

                # Reduce product quantity
                if item.variant:
                    variant = Variants.objects.get(id=item.variant.id)
                    variant.quantity -= item.quantity
                    variant.save()
                else:
                    product = Product.objects.get(id=item.product.id)
                    product.amount -= item.quantity
                    product.save()

            # Clear shopcart after order completion
            ShopCart.objects.filter(user_id=current_user.id).delete()
            messages.success(request, "Your order has been completed. Thank you!")
            return render(request, 'Order_Completed.html', {'ordercode': order.code, 'category': Category.objects.all()})

        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {
        'shopcart': shopcart,
        'category': Category.objects.all(),
        'total': total,
        'form': form,
        'profile': profile,
    }
    return render(request, 'Order_Form.html', context)
