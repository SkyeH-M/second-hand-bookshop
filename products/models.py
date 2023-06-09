from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    title = models.CharField(max_length=254)
    author = models.CharField(max_length=254)
    country = models.CharField(max_length=254)
    language = models.CharField(max_length=254)
    pages = models.IntegerField()
    release_year = models.IntegerField()
    blurb = models.TextField()
    has_quality = models.BooleanField(default=True, null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    averagerating = models.DecimalField(max_digits=4, decimal_places=2,
                                        null=True, blank=True, editable=False)
    image_link = models.ImageField(null=True, blank=True)
    # Very Academy
    users_wishlist = models.ManyToManyField(User, related_name="user_wishlist",
                                            blank=True, editable=False)

    def get_rating(self):
        """ Find average book rating """
        total = sum(int(review['stars']) for review in self.reviews.values())
        if self.reviews.count() > 0:
            return total / self.reviews.count()
        else:
            return 0

    def __str__(self):
        return self.title


class Quality(models.Model):
    """ Model to map relationship between quality of book and its price """
    class Meta:
        verbose_name_plural = 'Qualities'
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    price_factor = models.DecimalField(max_digits=3, decimal_places=2)

    def calculate_price(self):
        return self.product.price * self.price_factor

    def __str__(self):
        return self.name


class BookReview(models.Model):
    """
    A model for users to rate and reviews books, and for users
    to see ratings and reviews from all other users
    """
    class Meta:
        ordering = ['-date_added']

    STAR_CHOICES = (
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )

    product = models.ForeignKey(Product, related_name="reviews",
                                on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="user_reviews",
                             on_delete=models.CASCADE)
    stars = models.IntegerField(choices=STAR_CHOICES)
    content = models.TextField(blank=True, null=True, max_length=3000)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


@receiver(post_save, sender=BookReview)
def update_rating(sender, instance, created, **kwargs):
    instance.product.averagerating = instance.product.get_rating()
    instance.product.save()


@receiver(post_delete, sender=BookReview)
def update_rating(sender, instance, *args, **kwargs):
    instance.product.averagerating = instance.product.get_rating()
    instance.product.save()
