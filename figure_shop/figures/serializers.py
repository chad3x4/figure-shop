from rest_framework.serializers import ModelSerializer
from .models import Figure, Category, Notification, Order, Cart


class FigureSerializer(ModelSerializer):
    class Meta:
        model = Figure
        fields = ['id', 'name', 'cover', 'price']


class CartSerializer(ModelSerializer):
    figures = FigureSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['figures']


class OrderSerializer(ModelSerializer):
    figures = FigureSerializer(many=True)

    class Meta:
        model = Order
        fields = ['receiver_name', 'to_address', 'figures']
