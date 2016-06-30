#!/usr/bin/env python3.5

from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import Figure

#https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.AdminSite
class MyAdminSite(AdminSite):
    site_header = 'Dynamical Systems Administration'
    site_title = 'Dynamical Systems Administration'

class FigureAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    fieldsets = (
        ('Content', {
            'fields': ('author', 'title', 'summary', 'sourcecode', 'date', 'scanned_image'),
            'description': 'Enter the content of your article. Then select a picture on your computer.',
        }),
    )
    list_display = ('title', 'author', 'date')
    list_filter = ('title', 'author', 'date')

admin_site = MyAdminSite(name='myadmin')
admin_site.register(Figure, FigureAdmin)
admin.site.register(Figure, FigureAdmin)


