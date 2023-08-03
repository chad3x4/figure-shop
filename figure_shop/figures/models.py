from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# ImageField uploads image to MEDIA_ROOT/upload_to


class User(AbstractUser):
    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"

    avatar = models.ImageField(upload_to='avatar/%Y/%m', default=None)


class ItemBase(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=100, null=False, unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Figure(ItemBase):
    class Meta:
        ordering = ['id', 'name']
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"

    in_stock = models.IntegerField(default=None)
    cover = models.ImageField(upload_to='covers/%Y/%m', default=None)
    price = models.PositiveBigIntegerField()
    categories = models.ManyToManyField('Category', related_name='figures', blank=True)
    description = RichTextField()


class Category(ItemBase):
    pass


class Notification(ItemBase):
    class Meta:
        ordering = ['-created_date']
        verbose_name = "Thông báo"
        verbose_name_plural = "Thông báo"

    content = RichTextField()


class CartFigures(models.Model):
    class Meta:
        db_table = 'cart_figures'

    figure = models.ForeignKey('Figure', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)  # db_index makes auto index for FK field
    figures = models.ManyToManyField('Figure', related_name='carts', through=CartFigures, blank=True)


class OrdersFigures(models.Model):
    class Meta:
        db_table = 'order_figures'

    figure = models.ForeignKey('Figure', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(default=1)


class Order(models.Model):
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"

    receiver_name = models.CharField(max_length=50, null=False, default="Không xác định")
    to_address = models.TextField(max_length=255, null=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    status = models.CharField(max_length=50, default="Đang xử lý")
    active = models.BooleanField(default=True)
    is_purchased = models.BooleanField(default=False)
    figures = models.ManyToManyField('Figure', related_name='orders', through=OrdersFigures, blank=False)
    total_payment = models.PositiveBigIntegerField(default=0)

    def __str__(self):
        return "Đơn hàng #" + self.id.__str__()
