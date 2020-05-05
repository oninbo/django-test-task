import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import m2m_changed


class Shop(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to=os.path.join("images", "shop"))
    products = models.ManyToManyField(to='Product')

    def __str__(self):
        return self.title


def validate_price(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s is < 0'),
            params={'price': value},
        )


class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
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
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    children = models.ManyToManyField(to='self', related_name='parents',
                                      through='CategoryRelationship',
                                      through_fields=('parent', 'child'),
                                      blank=True,
                                      symmetrical=False
                                      )

    def is_self_parent(self):
        return len(self.parents.filter(id=self.id)) > 0

    def __str__(self):
        return self.title


class CategoryRelationship(models.Model):
    parent = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='child')
    child = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='parent')


def check_category_relationship_validity(sender, **kwargs):
    instance = kwargs["instance"]
    if instance.is_self_parent():
        raise ValidationError(_(f"Category {instance} can not be a parent to itself"))


m2m_changed.connect(check_category_relationship_validity)
