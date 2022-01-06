from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, primary_key=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=70)
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products')
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products')


RATING_CHOICES = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5')
)


class Review(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE,
                             related_name='reviews')
    text = models.TextField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    # rating = models.IntegerField(validators=[MinValueValidator(1),
    #                                          MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
