from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import LoginView
from .models import Court, Booking, UserBadminton
from .forms import CourtForm
from datetime import datetime, timedelta

# Create your views here.

def index(request):
    return render(request, 'court/index.html')

def court(request):
    return render(request, 'court/court.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # เปลี่ยนเส้นทางไปยังหน้า login แทน
    else:
        form = RegisterForm()
    
    return render(request, 'court/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'court/login.html'

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # ตรวจสอบบทบาทของผู้ใช้
            if user.is_superuser:  # ถ้าผู้ใช้เป็น admin
                return redirect('dashboard')  # เปลี่ยนเส้นทางไปยังหน้า dashboard
            elif hasattr(user, 'role'):  # ตรวจสอบว่ามี attribute 'role' หรือไม่
                if user.role in ['student', 'teacher']:
                    return redirect('booking')  # ถ้าบทบาทเป็น student หรือ teacher เปลี่ยนเส้นทางไปยังหน้า booking
            else:
                return redirect('booking')  # ถ้าไม่มีบทบาทที่ชัดเจนให้เปลี่ยนเส้นทางไปยัง booking

        else:
            # แสดงข้อความผิดพลาดถ้าล็อกอินไม่สำเร็จ
            error_message = "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง"
            return render(request, 'court/login.html', {'error': error_message})
    
    return render(request, 'court/login.html')

@login_required
def dashboard_view(request):
    if not request.user.is_superuser:
        return redirect('booking')

    courts = Court.objects.all()
    bookings = Booking.objects.all()
    users = UserBadminton.objects.all()  # เปลี่ยนจาก User เป็น UserBadminton

    return render(request, 'court/dashboard.html', {
        'courts': courts,
        'bookings': bookings,
        'users': users,
    })

@login_required
def booking_index(request):
    return render(request, 'court/booking.html')

@login_required
def booking_view(request):
    courts = Court.objects.filter(status='available')
    
    # Get user's first and last name
    first_name = request.user.first_name  # Assuming the user is authenticated
    last_name = request.user.last_name      # Assuming the user is authenticated

    if request.method == 'POST':
        selected_court_id = request.POST.get('court')
        selected_date = request.POST.get('date')  # Get the date from the form
        selected_time = request.POST.get('time')  # Get the time from the form

        if selected_court_id and selected_date and selected_time:
            court = get_object_or_404(Court, id=selected_court_id)

            # Split the selected time into start and end
            start_time_str, end_time_str = selected_time.split(' - ')

            # Convert date and time to datetime
            date_obj = datetime.strptime(selected_date, '%Y-%m-%d')
            start_time = datetime.strptime(start_time_str, '%H:%M')
            end_time = datetime.strptime(end_time_str, '%H:%M')

            # Combine date with time
            start_datetime = datetime.combine(date_obj.date(), start_time.time())
            end_datetime = datetime.combine(date_obj.date(), end_time.time())

            # Check if the booking is available for the selected time
            if Booking.objects.filter(court=court, start_time__lt=end_datetime, end_time__gt=start_datetime).exists():
                messages.error(request, 'สนามนี้ถูกจองแล้วในวันที่และเวลาที่เลือก.')
            else:
                # Create a new Booking instance with status "รอยืนยัน" (Pending)
                Booking.objects.create(court=court, user=request.user, start_time=start_datetime, end_time=end_datetime, status='รอยืนยัน')
                messages.success(request, f'จองสนาม {court.court_name} เรียบร้อยแล้วในวันที่ {selected_date} เวลา {selected_time}.')
                return redirect('my_bookings')  # Adjust to your redirection logic

    return render(request, 'court/booking.html', {
        'courts': courts,
        'first_name': first_name,  # Add first name to the context
        'last_name': last_name,      # Add last name to the context
    })

@login_required
def my_bookings_view(request):
    # ดึงการจองของผู้ใช้ที่ล็อกอินอยู่
    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'court/my_bookings.html', {
        'bookings': bookings,
    })

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def edit_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    if request.method == 'POST':
        court.name = request.POST['name']
        court.status = request.POST['status']
        court.save()
        return redirect('dashboard')  # เปลี่ยนเส้นทางไปยังหน้า dashboard

    return render(request, 'edit_court.html', {'court': court})

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        # รหัสเพื่อจัดการกับการอัปเดตการจอง
        pass  # ใส่รหัสที่คุณต้องการที่นี่
    return render(request, 'court/edit_booking.html', {'booking': booking})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(UserBadminton, id=user_id)  # เปลี่ยนเป็น UserBadminton
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.role = request.POST['role']
        user.save()
        return redirect('dashboard')  # เปลี่ยนเส้นทางไปยังหน้า dashboard

    return render(request, 'edit_user.html', {'user': user})

@login_required
def court_management(request):
    courts = Court.objects.all()  # หรือดึงข้อมูลที่คุณต้องการ
    return render(request, 'court/court_management.html', {'courts': courts})

@login_required
def booking_management(request):
    bookings = Booking.objects.all()  # หรือดึงข้อมูลที่คุณต้องการ
    return render(request, 'court/booking_management.html', {'bookings': bookings})

@login_required
def user_management(request):
    users = UserBadminton.objects.all()  # หรือดึงข้อมูลที่คุณต้องการ
    return render(request, 'court/user_management.html', {'users': users})

def delete_user_view(request, user_id):
    user = get_object_or_404(UserBadminton, id=user_id)
    user.delete()
    return redirect('user_management')  # Redirect to your user management page

@login_required
def edit_user_view(request, user_id):
    user = get_object_or_404(UserBadminton, id=user_id)  # Get the user or 404
    if request.method == 'POST':
        # Handle the form submission
        user.username = request.POST.get('username', user.username)  # Use the existing value if not provided
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.role = request.POST.get('role', user.role)
        user.save()
        return redirect('user_management')  # Redirect to user management after saving

    return render(request, 'court/edit_user.html', {'user': user})  # Ensure correct template path

def create_user(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']
        
        # สร้างผู้ใช้งานใหม่
        UserBadminton.objects.create(first_name=first_name, last_name=last_name, username=username, password=password, role=role)
        
        return redirect('user_management')  # เปลี่ยนเป็น URL ที่ต้องการไปหลังจากเพิ่มเสร็จ
    return render(request, 'court/create_user.html')  # เปลี่ยนชื่อไฟล์ตามต้องการ

def add_court(request):
    if request.method == 'POST':
        form = CourtForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('court_management')  # Adjust to your success redirect
    else:
        form = CourtForm()

    return render(request, 'court/add_court.html', {'form': form})

def edit_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)
    if request.method == 'POST':
        form = CourtForm(request.POST, instance=court)
        if form.is_valid():
            form.save()
            return redirect('court_management')  # Adjust to your success redirect
    else:
        form = CourtForm(instance=court)

    return render(request, 'court/edit_court.html', {'form': form})  # Adjust the template path if necessary

def delete_court(request, court_id):
    court = get_object_or_404(Court, id=court_id)  # Get the court object or return a 404 if not found
    if request.method == "POST":
        court.delete()  # Delete the court
        return redirect('court_management')  # Redirect to the court management page after deletion
    return render(request, 'delete_court.html', {'court': court})  # Optionally, render a confirmation page

def booking_management(request):
    bookings = Booking.objects.all()
    
    # Filter by status if selected
    selected_status = request.GET.get('status')
    if selected_status:
        bookings = bookings.filter(status=selected_status)
    
    return render(request, 'court/booking_management.html', {'bookings': bookings})

@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')

        # อัปเดตสถานะการจอง
        booking.status = new_status
        booking.save()

        messages.success(request, f'สถานะการจองสนาม {booking.court.court_name} เปลี่ยนเป็น {new_status}.')
    
    return redirect('booking_management')  # เปลี่ยนให้ตรงกับ URL ที่ต้องการรีไดเร็กต์

def manage_bookings(request):
    bookings = Booking.objects.all()  # ดึงข้อมูลการจองทั้งหมด
    return render(request, 'manage_bookings.html', {'bookings': bookings})  # เปลี่ยนชื่อไฟล์ HTML ตามที่คุณใช้