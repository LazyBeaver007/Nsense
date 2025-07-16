from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Patient, Doctor, Consultation, Prescription, PrescribedMedication

class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model.
    """
    class Meta:
        model = Patient
        fields = '__all__' 
        read_only_fields = ('id', 'created_at', 'updated_at')

class DoctorSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'full_name', 'hospital', 'specialization', 'username', 'password']
        read_only_fields = ('user',)
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        user = User.objects.create_user(username=username, password=password)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

class PrescribedMedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescribedMedication
        exclude = ('prescription',)

class PrescriptionSerializer(serializers.ModelSerializer):
    medications = PrescribedMedicationSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['id', 'consultation', 'created_at', 'medications']

    def create(self, validated_data):
        medications_data = validated_data.pop('medications')
        prescription = Prescription.objects.create(**validated_data)
        for medication_data in medications_data:
            PrescribedMedication.objects.create(prescription=prescription, **medication_data)
        return prescription


class ConsultationSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField()
    doctor = serializers.StringRelatedField()
    prescription = PrescriptionSerializer(read_only=True)

    class Meta:
        model = Consultation
        fields = ['id', 'patient', 'doctor', 'notes', 'created_at', 'prescription']


class ConsultationWriteSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'notes']


class PatientDetailSerializer(serializers.ModelSerializer):
    consultations = ConsultationSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'full_name', 'date_of_birth', 'contact_number', 
            'email', 'address', 'created_at', 'updated_at', 'consultations'
        ]

class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'full_name', 'date_of_birth', 'contact_number', 'email']
