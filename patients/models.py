from django.db import models
from django.contrib.auth.models import User
import uuid


class Patient(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='patient_profile', null=True)

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField(max_length=15, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Patient model.
        """
        return self.full_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    full_name = models.CharField(max_length=255)
    hospital = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.full_name}, {self.specialization}"
    

class Consultation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name='consultation')
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, related_name='consultation')
    notes = models.TextField(help_text="AI summarized notes form conversation")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consultation for {self.patient.full_name} on {self.created_at.strftime('%Y-%m-%d')}"


class Prescription(models.Model):
    """
    Represents a prescription given during a consultation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    consultation = models.OneToOneField(Consultation, on_delete=models.CASCADE, related_name='prescription')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.consultation.patient.full_name} from {self.created_at.strftime('%Y-%m-%d')}"

class PrescribedMedication(models.Model):
    """
    Represents a single medication within a prescription.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medications')

    drug_name = models.CharField(max_length=255)
    dosage = models.CharField(max_length=100, help_text="e.g., '500mg'")
    frequency = models.CharField(max_length=100, help_text="e.g., 'Twice a day'")
    duration_days = models.PositiveIntegerField(help_text="Duration of the medication in days.")

    def __str__(self):
        return f"{self.drug_name} ({self.dosage})"

