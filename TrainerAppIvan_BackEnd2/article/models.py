from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=255)
    brief_description = models.TextField()
    image1 = models.ImageField(upload_to='articles/images/')
    image2 = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='articles/images/', null=True, blank=True)
    paragraph1 = models.TextField(null=True, blank=True)
    paragraph2 = models.TextField(null=True, blank=True)
    paragraph3 = models.TextField(null=True, blank=True)
    paragraph4 = models.TextField(null=True, blank=True)
    paragraph5 = models.TextField(null=True, blank=True)
    paragraph6 = models.TextField(null=True, blank=True)
    paragraph7 = models.TextField(null=True, blank=True)
    paragraph8 = models.TextField(null=True, blank=True)
    paragraph9 = models.TextField(null=True, blank=True)
    paragraph10 = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


