from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import RegisterUserView, LoginView, booking, admin_dashboard, add_court, edit_court, court_management, delete_court
from django.contrib.auth.views import LogoutView
from .views import manage_user,add_user,edit_user,delete_user
from .views import manage_booking,edit_booking,delete_booking

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', LoginView, name='login'),
    path('register/', RegisterUserView, name='register_user'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  
    path('accounts/login/', LoginView, name='login'),  # Additional login route
    path('court/dashboard/', admin_dashboard, name='admin_dashboard'),  # Dashboard path
    # for User
    path('booking/', booking, name='booking'),

    # for Admin
    path('court/manage/court/', views.manage_court, name='manage_court'),
    path('court/manage/user/', views.manage_user, name='manage_user'),
    path('court/manage/booking/', views.manage_booking, name='manage_booking'),
    path('add/', add_court, name='add_court'),
    path('court/edit/<int:court_id>/', edit_court, name='edit_court'),  # Edit court path
    path('court/', court_management, name='court_management'),  # Management path
    path('delete/<int:court_id>/', delete_court, name='delete_court'), 
     path('court/manage/', views.manage_court, name='management_court'),  # Add this line
    path('court/manage/court/', views.manage_court, name='manage_court'),  # This can remain as is

    path('manage/user/', manage_user, name='manage_user'),
    path('manage/user/add/', add_user, name='add_user'),
    path('manage/user/edit/<int:user_id>/', edit_user, name='edit_user'),
    path('manage/user/delete/<int:user_id>/', delete_user, name='delete_user'),

     path('manage/booking/', manage_booking, name='manage_booking'),
    path('manage/booking/edit/<int:booking_id>/', edit_booking, name='edit_booking'),  # เพิ่มเส้นทางนี้
     path('manage/booking/delete/<int:booking_id>/', delete_booking, name='delete_booking'),  # เพิ่มเส้นทางนี้
]

# Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
