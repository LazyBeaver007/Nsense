from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, DoctorViewSet, ConsultationViewSet, PrescriptionViewSet


router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'consultations', ConsultationViewSet, basename='consultation')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')



urlpatterns = [
    path('', include(router.urls)),
]