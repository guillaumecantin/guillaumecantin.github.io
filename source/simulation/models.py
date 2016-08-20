from django.db import models

class Figure(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    sourcecode = models.TextField()
    date = models.DateField(blank=True, null=True)
    scanned_image = models.FileField(upload_to='scanned_images/')

class Animation(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    summary = models.TextField()
    source_code = models.TextField()
    date = models.DateField(blank=True, null=True)
    scanned_animation = models.FileField(upload_to='scanned_animations/')
    scanned_screen = models.FileField(upload_to='scanned_animations/')


