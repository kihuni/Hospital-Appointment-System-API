from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from .models import Role, Doctor, Appointment
from .serializers import RoleSerializer, DoctorSerializer, AppointmentSerializer
from .permissions import IsPatient, IsDoctor, IsAdmin, IsOwnerOrAdmin
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken




class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role.role
            },
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = serializer.validated_data  # validated_data is the User object
        refresh = RefreshToken.for_user(user)  # Generate tokens
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role.role
            }
        }, status=status.HTTP_200_OK)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=['post'], permission_classes=[IsDoctor])
    def update_availability(self, request, pk=None):
        doctor = self.get_object()
        if doctor.user != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        doctor.is_available = request.data.get('is_available', doctor.is_available)
        doctor.save()
        return Response(DoctorSerializer(doctor).data)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.user.is_authenticated:
            return [IsAuthenticated()]
        if self.action == 'create':
            return [IsAuthenticated(), IsPatient()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        elif self.action == 'list':
            if Role.objects.filter(user=self.request.user, role='DOCTOR').exists():
                return [IsAuthenticated(), IsDoctor()]
            elif Role.objects.filter(user=self.request.user, role='PATIENT').exists():
                return [IsAuthenticated(), IsPatient()]
            elif Role.objects.filter(user=self.request.user, role='ADMIN').exists():
                return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()
        if Role.objects.filter(user=user, role='PATIENT').exists():
            return Appointment.objects.filter(patient=user)
        elif Role.objects.filter(user=user, role='DOCTOR').exists():
            return Appointment.objects.filter(doctor__user=user)
        elif Role.objects.filter(user=user, role='ADMIN').exists():
            return Appointment.objects.all()
        return Appointment.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['patient'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)