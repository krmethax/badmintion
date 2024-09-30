from django.db import models

class Court(models.Model):
    court_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('not available', 'Not Available')])
    location = models.CharField(max_length=200, blank=True, null=True)  # Optional field
    manager = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_courts')  # ผู้จัดการสนาม

    def __str__(self):
        return self.court_name


class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords in production

    def __str__(self):
        return self.username


class Booking(models.Model):
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')])

    def __str__(self):
        return f"Booking by {self.user.username} on {self.booking_date} from {self.start_time} to {self.end_time}"

