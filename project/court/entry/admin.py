from django.contrib import admin
from django.contrib.auth.models import User
from .models import User, Court, Booking # นำเข้าโมเดลของคุณ

admin.site.register(User)  # ลงทะเบียนโมเดลของคุณกับ Admin
admin.site.register(Court)
admin.site.register(Booking)