from django.contrib import admin

from .models import Recruitment

"""
register Recruiment to admin
we can test it by admin panel
in urls search
admin/
"""

admin.site.register(Recruitment)
