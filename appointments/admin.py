from django.contrib import admin
from .models import Role, Doctor, Appointment

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Columns to show in the list view
    list_filter = ('role',)         # Filter by role (PATIENT, DOCTOR, ADMIN)
    search_fields = ('user__username', 'role')  # Search by username or role

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'is_available')  # Show user, specialty, availability
    list_filter = ('specialty', 'is_available')          # Filter by specialty, availability
    search_fields = ('user__username', 'specialty')      # Search by username or specialty

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'appointment_date', 'status', 'created_at')  # Show key fields
    list_filter = ('status', 'appointment_date')          # Filter by status, date
    search_fields = ('patient__username', 'doctor__user__username')  # Search by patient or doctor
    date_hierarchy = 'appointment_date'                   # Navigate by date