from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from .admin import admin_site
from . import views
from .views import index, figures_view, notifications_view, about_view, notification_detail, figure_detail, signin_view, \
    orders_view, figure_search, purchase_view, create_order, order_detail, logout_view, signin, signup_view, signup

router = DefaultRouter()
router.register('cart', views.CartViewSet)

urlpatterns = [
    path('', index),
    path('service/', include(router.urls)),
    path('signin/', signin_view),
    path('authenticate/', signin),
    path('signup/', signup_view),
    path('create_user/', signup),
    path('logout/', logout_view),
    path('figures/', figures_view),
    re_path(r'^figures/details/id=(?P<id>[0-9]|[1-9][0-9])/$', figure_detail),
    path('purchase/', purchase_view),
    path('search/', figure_search, name='figure_search'),
    path('orders/', orders_view),
    re_path(r'^orders/details/id=(?P<id>[0-9]|[1-9][0-9])/$', order_detail),
    path('create_order/',create_order),
    path('notifications/', notifications_view),
    re_path(r'^notifications/details/id=(?P<id>[0-9]|[1-9][0-9])/$', notification_detail),
    path('about/', about_view),
    path('admin/', admin_site.urls),
]
