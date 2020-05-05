import os
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
                                      blank=True
                                      )

    def __str__(self):
        return self.title


class CategoryRelationship(models.Model):
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='child')
    child = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='parent')

    def save(self, *args, **kwargs):
        if self.child.children_set.filter(id=self.parent.id):
            raise ValidationError(
                _(f"{self.child.title} category is a parent to {self.parent.title} and can not be set as a child."))
        elif self.parent.parents_set.filter(id=self.child.id):
            raise ValidationError(
                _(f"{self.parent.title} category is a child to {self.child.title} and can not be set as a parent."))
        else:
            super().save(*args, **kwargs)
