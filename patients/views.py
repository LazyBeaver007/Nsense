from rest_framework import viewsets
from .models import Patient, Doctor, Consultation, Prescription
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    PatientListSerializer, PatientDetailSerializer, DoctorSerializer, 
    ConsultationSerializer, 
    ConsultationWriteSerializer,
    PrescriptionSerializer
)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('full_name')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PatientDetailSerializer
        return PatientListSerializer
    
    def get_queryset(self):
        """
        This view should return a list of all the patients
        for the currently authenticated doctor.
        """
        user = self.request.user
        if hasattr(user, 'doctor_profile'):
            # User is a doctor, return patients they have consulted
            doctor = user.doctor_profile
            return Patient.objects.filter(consultations__doctor=doctor).distinct()
        elif hasattr(user, 'patient_profile'):
            # User is a patient, return only their own profile
            return Patient.objects.filter(pk=user.patient_profile.pk)
        return Patient.objects.none()

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all().order_by('full_name')
    serializer_class = DoctorSerializer

class ConsultationViewSet(viewsets.ModelViewSet):
    queryset = Consultation.objects.all().order_by('-created_at')

  
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConsultationWriteSerializer 
        return ConsultationSerializer 
    
    def get_queryset(self):
        """
        Filter consultations based on the logged-in user.
        """
        user = self.request.user
        if hasattr(user, 'doctor_profile'):
            return Consultation.objects.filter(doctor=user.doctor_profile)
        elif hasattr(user, 'patient_profile'):
            return Consultation.objects.filter(patient=user.patient_profile)
        return Consultation.objects.none()
    
    def perform_create(self, serializer):
        """
        Automatically assign the logged-in doctor to the consultation.
        """
        if hasattr(self.request.user, 'doctor_profile'):
            serializer.save(doctor=self.request.user.doctor_profile)
        else:
            # Handle case where a non-doctor tries to create a consultation if needed
            pass


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().order_by('-created_at')
    serializer_class = PrescriptionSerializer
    http_method_names = ['get', 'post', 'head', 'options'] # More explicit way to limit actions
