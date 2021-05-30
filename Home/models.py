from django.db import models
from ckeditor.fields import RichTextField
from django.forms import ModelForm, TextInput, Textarea

# Create your models here.


class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keyword = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    company = models.CharField(max_length=150)
    address = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    fax = models.CharField(max_length=15, blank=True)
    email = models.CharField(max_length=50, blank=True)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpmail = models.CharField(blank=True, max_length=50)
    smtpassword = models.CharField(blank=True, max_length=10)
    smtport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(max_length=50, blank=True)
    instagram = models.CharField(max_length=50, blank=True)
    twitter = models.CharField(max_length=50, blank=True)
    aboutus = RichTextField(blank=True, null=True)
    aboutpage = RichTextField(blank=True, null=True)
    contact = RichTextField(blank=True, null=True)
    reference = RichTextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(max_length=50, blank=True)
    note = models.CharField(max_length=150, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactForm(ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'input ', 'placeholder': 'Name & Surname...'}),
            'email': TextInput(attrs={'class': 'input ', 'placeholder': 'Your Email...'}),
            'subject': TextInput(attrs={'class': 'input ', 'placeholder': 'Your Subject...'}),
            'message': Textarea(attrs={'class': 'input ', 'placeholder': 'Your Message', 'rows': '5'}),
        }


class SliderImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    offer = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='slider_image/')

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.title


class OfferImage(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    offer = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='slider_image/')

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.title
