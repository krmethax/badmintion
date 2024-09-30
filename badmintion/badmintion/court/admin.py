from django.contrib import admin
from django.contrib.auth.models import User
from .models import Booking,Court,UserBadminton  # นำเข้าโมเดลของคุณ

admin.site.register(Booking)
admin.site.register(Court)
admin.site.register(UserBadminton)