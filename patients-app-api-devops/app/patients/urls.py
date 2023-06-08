"""
URL mappings for the patients app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from patients import views

router = DefaultRouter()
router.register('patientss', views.PatientsViewSet)
router.register('tags', views.TagViewSet)
router.register('treatment', views.TreatmentViewSet)
router.register('all',views.AllPatientsViewSet)
app_name = 'patients'

urlpatterns = [
    path('', include(router.urls)) 
]
