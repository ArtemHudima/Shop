from django.shortcuts import render, get_object_or_404
from .forms import ReviewForm
from django.contrib import messages
from django.db import models
# Create your views here.
from django.shortcuts import render
from .models import Product, Category, Review
from django.core.mail import send_mail
from django.http import JsonResponse
from django.template.loader import render_to_string
# from django.db.models import Q
#
# def home(request):
#     query = request.GET.get('q', '')
#     if query:
#         products = Product.objects.filter(
#             Q(name__icontains=query) | Q(description__icontains=query)
#         )
#     else:
#         products = Product.objects.all()
#
#     categories = Category.objects.all()
#     return render(request, 'shop/home.html', {
#         'products': products,
#         'categories': categories,
#         'query': query
#     })

from django.core.paginator import Paginator
from django.db.models import Q

def home(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.all()

    paginator = Paginator(products, 9)  # 8 товарів на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    return render(request, 'shop/home.html', {
        'products': page_obj,  # важливо!
        'categories': categories,
        'query': query,
        'page_obj': page_obj,
    })




def ajax_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    ) if query else Product.objects.all()

    html = render_to_string('shop/partials/product_list.html', {'products': products})
    return JsonResponse({'html': html})







def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    user_review = None

    if request.user.is_authenticated:
        try:
            user_review = product.reviews.get(user=request.user)
        except Review.DoesNotExist:
            user_review = None

    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if not user_review and form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            messages.success(request, "Відгук додано!")
            return redirect('product_detail', pk=pk)
    else:
        form = ReviewForm()
    avg_rating = product.reviews.aggregate(models.Avg('rating'))['rating__avg']
    return render(request, 'shop/product_detail.html', {
            'product': product,
            'reviews': reviews,
            'form': form,
            'user_review': user_review,
            'avg_rating': avg_rating
        })


from django.shortcuts import redirect
from .cart import Cart


def add_to_cart(request, pk):
    cart = Cart(request)
    cart.add(pk)
    return redirect('cart_detail')

def decrease_item_cart(request, pk):
    cart = Cart(request)
    cart.decrease(pk)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'shop/cart.html', {'cart_items': cart.items(), 'total': cart.total_price()})


def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')


from .forms import OrderForm
from .models import Order, OrderItem
from django.contrib import messages


def checkout(request):
    cart = Cart(request)
    if not cart.items():
        messages.warning(request, "Ваш кошик порожній!")
        return redirect('home')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total=cart.total_price()
            )
            for item in cart.items():
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    price=item['product'].price
                )
            cart.clear()

            order_items_text = ""
            for item in order.items.all():
                order_items_text += f"- {item.product.name} (x{item.quantity}): {item.get_total_price()} грн\n"

            email_message = f"""
            Дякуємо за ваше замовлення, {order.name}!

            Номер замовлення: {order.id}
            Дата: {order.created_at.strftime('%Y-%m-%d %H:%M')}
            Загальна сума: {order.total} грн

            Замовлені товари:
            {order_items_text}

            Доставка за адресою:
            {order.address}

            Якщо це були не ви — проігноруйте лист.

            З повагою,
            Команда MiniShop
            """

            send_mail(
                subject=f'Підтвердження замовлення №{order.id}',
                message=email_message,
                from_email=None,  # DEFAULT_FROM_EMAIL використовується
                recipient_list=[request.user.email] if request.user.is_authenticated and request.user.email else [
                    'admin@example.com'],
                fail_silently=False,
            )
            messages.success(request, "Замовлення оформлено успішно!")
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'shop/checkout.html', {
        'form': form,
        'cart_items': cart.items(),
        'total': cart.total_price()
    })



def categories_list(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    categories = Category.objects.all()
    return render(request, 'shop/categories.html', {
        'products': products,
        'categories': categories,
        'query': query
    })