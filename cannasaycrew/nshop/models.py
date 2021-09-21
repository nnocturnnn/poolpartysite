from os import pathconf
from django.db import models
from django.db.models.fields.files import ImageField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

User = get_user_model()
# class User(AbstractUser):
#     def __str__(self):
#         return self.email

# Create your models here.

class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Имя")
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='static/',verbose_name='Изображение')
    deskription = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

    def __str__(self) -> str:
        return self.title

class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
    product = models.ForeignKey(Product, verbose_name='Продукт', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая Цена')

    def __str__(self) -> str:
        return f"Продукт {self.product.title}"


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_product = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая Цена')

    def __str__(self) -> str:
        return self.id


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    addres = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self) -> str:
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"

