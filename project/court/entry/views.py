from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import Court, User, Booking
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django import forms
from .forms import UserForm,BookingForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

@login_required
def booking(request):
    return render(request, 'booking.html')

# ตั้งชื่อฟังก์ชันได้ตามสะดวก
def RegisterUserView(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "ลงทะเบียนสำเร็จ! คุณสามารถเข้าสู่ระบบได้แล้ว.")
            return redirect('/login')  # เปลี่ยนไปยังหน้าล็อกอินหลังจากลงทะเบียนสำเร็จ
        else:
            # ตรวจสอบว่ามีข้อผิดพลาดเฉพาะ
            if 'password' in form.errors:
                messages.error(request, "รหัสผ่านคาดเดาง่ายเกินไปหรือไม่ตรงตามเงื่อนไข.")
            elif 'username' in form.errors:
                messages.error(request, "มีชื่อผู้ใช้ในระบบแล้ว กรุณาเลือกชื่อผู้ใช้อื่น.")
            else:
                messages.error(request, "กรุณาแก้ไขข้อผิดพลาดด้านล่าง.")
    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def LoginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)  # ตรวจสอบชื่อผู้ใช้และรหัสผ่าน
            
            # ตรวจสอบ username และ password
            if username == 'admin' and password == 'admin@badmintion':
                auth_login(request, user)  # ทำการล็อกอิน
                messages.success(request, "คุณได้เข้าสู่ระบบในฐานะ admin แล้ว.")
                return redirect('/court/dashboard')  # เปลี่ยนไปยังหน้าคอร์ต/dashboard หลังจากล็อกอินสำเร็จ
            elif user is not None:
                auth_login(request, user)  # ทำการล็อกอิน
                messages.success(request, f"คุณได้เข้าสู่ระบบในฐานะ {username} แล้ว.")
                # ตรวจสอบพารามิเตอร์ next
                next_url = request.GET.get('next', '/booking')  # ถ้ามี next ใช้ URL ที่ส่งมา ถ้าไม่มีให้ไปที่ /booking
                return redirect(next_url)  # เปลี่ยนไปยังหน้าที่ผู้ใช้ต้องการ
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.")
        else:
            messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.username == 'admin':  # ตรวจสอบชื่อผู้ใช้
        courts = Court.objects.all()
        users = User.objects.all()
        bookings = Booking.objects.all()

        context = {
            'courts': courts,
            'users': users,
            'bookings': bookings
        }

        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, "คุณไม่มีสิทธิ์เข้าถึงหน้าแดชบอร์ด.")
        return redirect('/login')  # เปลี่ยนไปยังหน้าล็อกอินถ้าไม่มีสิทธิ์

# Manage courts
def manage_court(request):
    courts = Court.objects.all()
    return render(request, 'manage_court.html', {'courts': courts})

# Manage users
def manage_user(request):
    users = User.objects.all()
    return render(request, 'manage_user.html', {'users': users})

# Manage bookings
def manage_booking(request):
    bookings = Booking.objects.all()
    return render(request, 'manage_booking.html', {'bookings': bookings})

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['court_name', 'status']

def add_court(request):
    if request.method == 'POST':
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "เพิ่มข้อมูลสนามเรียบร้อยแล้ว.")
            return redirect('manage_court')  # Change this to 'court_management'
    else:
        form = CourtForm()

    return render(request, 'add_court.html') 

def edit_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    if request.method == 'POST':
        court.court_name = request.POST.get('court_name')
        court.status = request.POST.get('status')
        court.save()  # บันทึกข้อมูลที่แก้ไข
        messages.success(request, "แก้ไขข้อมูลสนามเรียบร้อยแล้ว.")
        return redirect('management_court')  # เปลี่ยนไปยังหน้าจัดการสนาม
    return render(request, 'edit_court.html', {'court': court})

def court_management(request):
    courts = Court.objects.all()  # ดึงข้อมูลสนามทั้งหมดจากฐานข้อมูล
    return render(request, 'management_court.html', {'courts': courts})  # เปลี่ยนไปยังเทมเพลตที่คุณใช้

def delete_court(request, court_id):  # ตรวจสอบให้แน่ใจว่าคุณใช้ court_id
    court = get_object_or_404(Court, id=court_id)
    court.delete()
    messages.success(request, "ลบข้อมูลสนามเรียบร้อยแล้ว.")
    return redirect('management_court')  # เปลี่ยนเส้นทางหลังจากลบ

def manage_user(request):
    users = User.objects.all()  # ดึงข้อมูลผู้ใช้ทั้งหมด
    return render(request, 'manage_user.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_user')  # กลับไปที่หน้าจัดการผู้ใช้
    else:
        form = UserForm()
    return render(request, 'add_user.html', {'form': form})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_user')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_user')
    return render(request, 'delete_user.html', {'user': user})

def manage_booking(request):
    bookings = Booking.objects.all()  # ดึงข้อมูลการจองทั้งหมด
    return render(request, 'manage_booking.html', {'bookings': bookings})

def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('manage_booking')  # เปลี่ยนเป็น URL ที่ต้องการ
    else:
        form = BookingForm(instance=booking)

    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('manage_booking')  # เปลี่ยนเส้นทางไปยังหน้าจัดการการจอง