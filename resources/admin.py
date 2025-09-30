from django.contrib import admin

from .models import Resources

"""
register Resource to admin
we can test it by admin panel
in urls search
admin/
"""

admin.site.register(Resources)
