from django.db import models

# Create your models here.


class Category(models.Model):

    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    parent = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.CASCADE, related_name='children')
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    keyword = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/', blank=True)
    price = models.FloatField()
    amount = models.IntegerField()
    minamount = models.IntegerField()
    detail = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    slug = models.SlugField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
