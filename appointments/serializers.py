from rest_framework import serializers
from .models import Role, Doctor, Appointment
from django.contrib.auth.models import User
from .models import Role
from django.contrib.auth import authenticate



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    email = serializers.EmailField(required=True)
    role = serializers.ChoiceField(choices=Role.ROLE_CHOICES, default='PATIENT', required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role', 'PATIENT')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        Role.objects.create(user=user, role=role)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class RoleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Role
        fields = ['id', 'user', 'role']

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Doctor
        fields = ['id', 'user', 'specialty', 'is_available']

class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    date = serializers.DateTimeField(source='appointment_date')

    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'date', 'status', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}  # Automatically set by model
        }

    def validate(self, data):
        if 'patient' not in data and not self.context.get('request').user.is_authenticated:
            raise serializers.ValidationError({"patient": "Patient is required."})
        return data