from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import register, login_view, booking_index, logout_view, dashboard_view
from django.contrib.auth import views as auth_views
from .views import court_management, booking_management
from .views import user_management, delete_user_view, edit_user_view, create_user
from .views import add_court, delete_court
from .views import booking_view, my_bookings_view, update_booking_status, manage_bookings
from .views import reset_password

urlpatterns = [
    path('', views.index, name='index'),
    path('court/', views.court, name='court'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'), 
    path('booking/', booking_view, name='booking'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    path('edit_court/<int:court_id>/', views.edit_court, name='edit_court'), 
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('edit_user/<int:user_id>/', edit_user_view, name='edit_user'),  # ใช้ edit_user_view
    path('court_management/', court_management, name='court_management'),
    path('booking_management/', booking_management, name='booking_management'),
    path('user_management/', user_management, name='user_management'),
    path('user/delete/<int:user_id>/', delete_user_view, name='delete_user'),
    path('create_user/', create_user, name='create_user'),
    path('add-court/', add_court, name='add_court'),
    path('delete-court/<int:court_id>/', delete_court, name='delete_court'),
    path('my-bookings/', my_bookings_view, name='my_bookings'),
    path('update_booking_status/<int:booking_id>/', update_booking_status, name='update_booking_status'),
    path('manage_bookings/', manage_bookings, name='manage_bookings'),
    path('booking_detail/', views.booking_detail_view, name='booking_detail'),
    path('reset-password/', reset_password, name='reset_password'),
]

# เพิ่มการให้บริการไฟล์มีเดียในโหมด Development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

