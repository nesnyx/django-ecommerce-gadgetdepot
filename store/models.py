from django.db import models
from django.urls import reverse
from category.models import Category
from accounts.models import Account
from django.db.models import Avg,Count
# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    description = models.TextField(max_length=500,blank=True)
    price = models.IntegerField()
    images_product = models.ImageField(upload_to='photos/products')
    qty = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product_name

    def get_url(self): return reverse('product_detail', args=[self.category.slug, self.slug])

    def averageReview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count
class VariationManager(models.Manager):
    def firstSpec(self):
        return super(VariationManager,self).filter(variation_category='4/64', is_active=True)
    def secondSpec(self):
        return super(VariationManager,self).filter(variation_category='8/128', is_active=True)

variation_category_list = (
    ('4/64','4/64'),
    ('8/128','8/128')
)

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=20,choices=variation_category_list)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)
    objects = VariationManager()
    
    def __unicode__(self) -> str:
        return self.product
    
class Specification(models.Model):
    spec_name = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.spec_name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.subject
