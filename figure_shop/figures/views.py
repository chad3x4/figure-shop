from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Figure, Notification, Order, Cart, User
from .serializers import CartSerializer, OrderSerializer


# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.all()
        return render(request, 'home/base-user.html', {'my_figures': my_figures, 'user': user, 'cart': cart})
    else:
        return render(request, 'home/base-guest.html')


def signin_view(request):
    return render(request, 'home/signin.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            message = 'Tên đăng nhập hoặc mật khẩu chưa chính xác'
            return render(request, 'home/signin.html', {'message': message})
    else:
        return redirect(signin_view)


def signup_view(request):
    return render(request, 'home/signup.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        mail = request.POST['mail']
        password = request.POST['password']
        cf_password = request.POST['cfpassword']
        if cf_password == password:
            if User.objects.filter(username=username).exists():
                message = 'Tên tài khoản đã được sử dụng'
                return render(request, 'home/signup.html', {'message': message})
            else:
                user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname, email=mail, is_staff=0)
                user.save()
                Cart.objects.create(user=user)
                return redirect('/signin')
        else:
            message = 'Mật khẩu nhập lại không trùng khớp'
            return render(request, 'home/signup.html', {'message': message})
    else:
        return render(request, 'signup.html')


def modes_view(request):
    return render(request, 'admin/admin-mode-selection.html')


def statistics_view(request):
    orders = Order.objects.all()
    months = {
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
        9: 0,
        10: 0,
        11: 0,
        12: 0
    }
    for order in orders:
        month = order.created_date.month
        months[month] += order.total_payment
    if request.user.is_superuser:
        return render(request, 'admin/admin-statistics.html', {'months': months})
    else:
        return redirect(index)


def logout_view(request):
    logout(request)
    return redirect(index)


def figures_view(request):
    figures = Figure.objects.filter(in_stock__gt=0)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.filter(in_stock__gt=0)
        return render(request, 'home/user-figures.html', {'figures': figures, 'my_figures': my_figures, 'cart': cart})
    else:
        return render(request, 'home/guest-figures.html', {'figures': figures})


def figure_detail(request, id):
    figure = Figure.objects.get(pk=id)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.filter(in_stock__gt=0)
        return render(request, 'home/user-fig-details.html', {'figure': figure, 'my_figures': my_figures, 'cart': cart})
    else:
        return render(request, 'home/guest-fig-details.html', {'figure': figure})


@login_required(login_url='/signin/')
def figure_search(request):
    keyword = request.GET['keyword']
    figures = Figure.objects.filter(in_stock__gt=0, name__icontains=keyword)
    cart = Cart.objects.filter(user=request.user).first()
    my_figures = cart.figures.filter(in_stock__gt=0)
    return render(request, 'home/user-figures.html', {'figures': figures, 'my_figures': my_figures, 'cart': cart, 'keyword': keyword})


@login_required(login_url='/signin/')
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    cart = Cart.objects.filter(user=request.user).first()
    my_figures = cart.figures.filter(in_stock__gt=0)
    return render(request, 'home/user-orders.html', {'orders': orders, 'my_figures': my_figures, 'cart': cart})


def notifications_view(request):
    notifications = Notification.objects.all()
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.filter(in_stock__gt=0)
        return render(request, 'home/user-notifications.html', {'notifications': notifications, 'my_figures': my_figures, 'cart':cart})
    else:
        return render(request, 'home/guest-notifications.html', {'notifications': notifications})


def notification_detail(request, id):
    notification = Notification.objects.get(pk=id)
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.filter(in_stock__gt=0)
        return render(request, 'home/user-noti-details.html', {'notification': notification, 'my_figures': my_figures, 'cart': cart})
    else:
        return render(request, 'home/guest-noti-details.html', {'notification': notification})


def about_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        my_figures = cart.figures.filter(in_stock__gt=0)
        return render(request, 'home/user-about.html', {'my_figures': my_figures, 'cart': cart})
    else:
        return render(request, 'home/guest-about.html')


# def login(request):
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#
#     else:
#         return HttpResponse('Account not exists!!!')


@login_required(login_url='/signin/')
def purchase_view(request):
    total_payment = 0
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    purchased_figures = cart.figures.filter(in_stock__gt=0)
    for figure in purchased_figures:
        cart_figure = cart.cartfigures_set.get(figure=figure)
        quantity = cart_figure.quantity
        total_payment += figure.price * quantity

    return render(request, 'home/purchase.html',
                  {'user': user, 'figures': purchased_figures, 'cart': cart, 'total_payment': total_payment})


def order_detail(request, id):
    order = Order.objects.get(pk=id)
    order_figures = order.figures.all()
    return render(request, 'home/user-order-details.html', {'order': order, 'order_figures': order_figures})


@login_required(login_url='/signin/')
def create_order(request):
    total_payment = 0
    receiver_name = request.GET['receiver-name']
    to_address = request.GET['to-address']
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    purchased_figures = cart.figures.filter(in_stock__gt=0)
    for figure in purchased_figures:
        cart_figure = cart.cartfigures_set.get(figure=figure)
        quantity = cart_figure.quantity
        total_payment += figure.price * quantity
    new_order = Order.objects.create(receiver_name=receiver_name, to_address=to_address, user=user, total_payment=total_payment)
    new_order.figures.set(purchased_figures)
    for figure in purchased_figures:
        cart_figure = cart.cartfigures_set.get(figure=figure)
        quantity = cart_figure.quantity
        order_figure = new_order.ordersfigures_set.get(figure=figure)
        order_figure.quantity = quantity
        order_figure.save()
        item = Figure.objects.get(id=figure.id)
        item.in_stock -= quantity
        item.save()
        cart.figures.remove(figure)
    new_order.save()

    return redirect(orders_view)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    @action(methods=['get'], detail=True, url_path="add_to_cart")
    def add_to_cart(self, request, pk):
        try:
            figure = Figure.objects.get(pk=pk)
            cart = Cart.objects.filter(user=request.user).first()
            if cart.cartfigures_set.filter(figure=figure):
                cart_figure = cart.cartfigures_set.get(figure=figure)
                if cart_figure.quantity < figure.in_stock:
                    cart_figure.quantity += 1
                    cart_figure.save()
                else:
                    pass
            else:
                cart.figures.add(figure)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path="remove_from_cart")
    def remove_from_cart(self, request, pk):
        try:
            figure = Figure.objects.get(pk=pk)
            cart = Cart.objects.filter(user=request.user).first()
            cart.figures.remove(figure)
            cart.save()
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_200_OK)