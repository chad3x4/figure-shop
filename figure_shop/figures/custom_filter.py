from django import template

register = template.Library()


@register.filter
def with_figure(cart, figure):
    return cart.cartfigures_set.get(figure=figure)


@register.filter
def order_with_figure(order, figure):
    return order.ordersfigures_set.get(figure=figure)


@register.filter
def divide(value, arg):
    return value / arg
