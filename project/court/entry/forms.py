# entry/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Booking


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # ระบุฟิลด์ที่ต้องการ

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()  # ใช้ PasswordInput สำหรับฟิลด์รหัสผ่าน

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['court', 'user', 'booking_date', 'start_time', 'end_time', 'status']  # ใส่ฟิลด์ที่ต้องการ