from django.db import models

class Shop(models.Model):
    title = models.CharField()
    description = models.CharField(max_length=200)
    imageURL = models.ImageField(upload_to="images/shop")
    def __str__(self):
        return self.title
