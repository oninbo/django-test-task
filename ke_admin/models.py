import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Shop(models.Model):
    title = models.CharField()
    description = models.TextField()
    image = models.ImageField(upload_to=os.path.join("images", "shop"))
    products = models.ManyToManyField(to='Product')

    def __str__(self):
        return self.title

def validate_price(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is < 0'),
            params={'value': value},
        )

class Product(models.Model):
    title = models.CharField()
    description = models.TextField()
    amount = models.PositiveIntegerField()
    price = models.FloatField(validators=[validate_price])
    active = models.BooleanField()

    def __str__(self):
        return self.title


class ImageProduct(models.Model):
    image = models.ImageField(upload_to=os.path.join("images", "product"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField()
    description = models.TextField()
