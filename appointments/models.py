from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Role(models.Model):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('ADMIN', 'Admin'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.specialty}"

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
    )
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.patient.username} with {self.doctor.user.username} on {self.appointment_date}"