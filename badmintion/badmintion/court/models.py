from django.db import models
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserBadmintonManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)  # This handles password hashing
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

class UserBadminton(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=[
        ('admin', 'ผู้ดูแลระบบ'),
        ('teacher', 'ครู'),
        ('student', 'นักเรียน')
    ])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)  # Track last login time

    objects = UserBadmintonManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']  # Required fields for createsuperuser

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_userbadminton_set',  # Change this related name
        blank=True,
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_userbadminton_set',  # Change this related name
        blank=True,
    )

    def __str__(self):
        return self.username

class Court(models.Model):
    id = models.AutoField(primary_key=True)
    court_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=11, choices=[
        ('available', 'ว่าง'),
        ('unavailable', 'ไม่ว่าง')
    ])

    def __str__(self):
        return self.court_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'รอการยืนยัน'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('canceled', 'ยกเลิก'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserBadminton, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  

    def clean(self):
        """ตรวจสอบเวลาการจอง"""
        if self.end_time <= self.start_time:
            raise ValidationError("เวลาสิ้นสุดต้องมากกว่าเวลาเริ่มต้น")
        if (self.end_time - self.start_time) != timedelta(hours=1):
            raise ValidationError("ระยะเวลาการจองต้องเป็น 1 ชั่วโมง")

    def __str__(self):
        return f"การจอง {self.id} โดย {self.user.username} สำหรับสนาม {self.court.court_name} ตั้งแต่ {self.start_time} ถึง {self.end_time}"
