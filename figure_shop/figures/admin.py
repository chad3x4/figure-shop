from django.contrib import admin
from django import forms
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Figure, User, Notification, Order, Category, Cart


class FigureForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Figure
        fields = ['name', 'in_stock', 'cover', 'price', 'description']


class FigureAdmin(admin.ModelAdmin):
    form = FigureForm
    actions_on_top = False
    save_and_add_another = False
    save_and_continue_editing = False
    list_display = ['id', 'name', 'price']
    list_display_links = ('id', 'name')
    readonly_fields = ['cover_uploaded']

    def cover_uploaded(self, figure):
        if figure:
            return mark_safe("<img src='/static/{url}' alt='{alt}' width='120' />"
                             .format(url=figure.cover.name, alt=figure.name))

    class Media:
        css = {
            'all': ('/static/css/admin-style.css', )
        }
    #     js = ('/static/js/script.js', )


class UserForm(forms.ModelForm):
    class Meta:
        fields = ['username', 'email', 'is_staff', 'first_name', 'last_name', ]


class UserAdmin(admin.ModelAdmin):
    form = UserForm
    actions_on_top = False
    list_display = ['username', 'first_name', 'last_name', ]

    def has_add_permission(self, request):
        return False

    class Media:
        css = {
            'all': ('/static/css/admin-style.css', )
        }


class NotificationForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Notification
        fields = ['name', 'content']


class NotificationAdmin(admin.ModelAdmin):
    form = NotificationForm
    actions_on_top = False
    save_and_add_another = False
    save_and_continue_editing = False

    class Media:
        css = {
            'all': ('/static/css/admin-style.css', )
        }


class OrderForm(forms.ModelForm):
    class Meta:
        fields = ['receiver_name', 'to_address', 'status', 'is_purchased', 'total_payment']


class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    actions_on_top = False
    save_and_add_another = False
    save_and_continue_editing = False
    show_full_result_count = False

    def has_change_permission(self, request, obj=None):
        return False

    class Media:
        css = {
            'all': ('/static/css/admin-style.css', )
        }


class FigureShopAdminSite(admin.AdminSite):
    site_title = "Administrator"
    site_header = "Figure Shop"
    index_title = "Hệ thống quản lý cửa hàng"

    def get_urls(self):
        return [
        ] + super().get_urls()


admin_site = FigureShopAdminSite("Figure Shop")

# Register your models here.
admin_site.register(Figure, FigureAdmin)
admin_site.register(User, UserAdmin)
admin_site.register(Notification, NotificationAdmin)
admin_site.register(Order, OrderAdmin)
