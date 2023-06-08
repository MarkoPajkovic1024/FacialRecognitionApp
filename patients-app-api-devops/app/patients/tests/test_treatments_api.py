"""
Tests for the treatment API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Treatment,
    Patients,
)

from patients.serializers import TreatmentSerializer


TREATMENTS_URL = reverse('patients:treatment-list')


def detail_url(treatment_id):
    """Create and return an treatment detail URL."""
    return reverse('patients:treatment-detail', args=[treatment_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTreatmentApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving treatment."""
        res = self.client.get(TREATMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTreatmentApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_treatment(self):
        """Test retrieving a list of treatment."""
        Treatment.objects.create(user=self.user, name='Kale')
        Treatment.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(TREATMENTS_URL)

        treatments = Treatment.objects.all().order_by('-name')
        serializer = TreatmentSerializer(treatments, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_treatments_limited_to_user(self):
        """Test list of treatments is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Treatment.objects.create(user=user2, name='Breathing')
        treatment = Treatment.objects.create(user=self.user, name='Pepper')

        res = self.client.get(TREATMENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], treatment.name)
        self.assertEqual(res.data[0]['id'], treatment.id)

    def test_update_treatment(self):
        """Test updating an treatment."""
        treatment = Treatment.objects.create(user=self.user, name='advil')

        payload = {'name': 'aspirin'}
        url = detail_url(treatment.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        treatment.refresh_from_db()
        self.assertEqual(treatment.name, payload['name'])

    def test_delete_treatment(self):
        """Test deleting an treatment."""
        treatment = Treatment.objects.create(user=self.user, name='peniciline')

        url = detail_url(treatment.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        treatments = Treatment.objects.filter(user=self.user)
        self.assertFalse(treatments.exists())

    def test_filter_treatment_assigned_to_patients(self):
        """Test listing tratments to those assigned to patients."""
        in1 = Treatment.objects.create(user=self.user, name='Apples')
        in2 = Treatment.objects.create(user=self.user, name='Turkey')
        patients = Patients.objects.create(
            # title='Apple Crumble',
            # time_minutes=5,
            # price=Decimal('4.50'),
            # user=self.user,
            user=self.user,
            first_name='Sample Apples name',
            last_name='Sample patients last name',
            age=5,
            med_list='samole med list',
            phone_number='+12345678',
            date_of_birth='2006-08-21',
            street_address="sample address",
            city_address="sample city",
            zipcode_address="sample zip",
            state_address="sample state",
            creation_date='2006-08-21',
            modified_date='2006-08-22',
            description='Sample receipe description.',
            gender='Male',
            emergency_contact_name='Sample contact name',
            emergency_phone_number='+12345678',
            relationship='Father',
            is_in_hospital=True,
        )

        patients.treatment.add(in1)

        res = self.client.get(TREATMENTS_URL, {'assigned_only': 1})

        s1 = TreatmentSerializer(in1)
        s2 = TreatmentSerializer(in2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_treatment_unique(self):
        """Test filtered treatmentreturns a unique list."""
        ing = Treatment.objects.create(user=self.user, name='Eggs')
        Treatment.objects.create(user=self.user, name='Lentils')
        patients1 = Patients.objects.create(
            user=self.user,
            first_name='Sample Eggs name',
            last_name='Sample patients last name',
            age=5,
            med_list='samole med list',
            phone_number='+12345678',
            date_of_birth='2006-08-21',
            street_address="sample address",
            city_address="sample city",
            zipcode_address="sample zip",
            state_address="sample state",
            creation_date='2006-08-21',
            modified_date='2006-08-22',
            description='Sample receipe description.',
            gender='Male',
            emergency_contact_name='Sample contact name',
            emergency_phone_number='+12345678',
            relationship='Father',
            is_in_hospital=True,
        )
        patients2 = Patients.objects.create(
            user=self.user,
            first_name='Samples of Eggs name',
            last_name='Sample patients last name',
            age=5,
            med_list='samole med list',
            phone_number='+12345678',
            date_of_birth='2006-08-21',
            street_address="sample address",
            city_address="sample city",
            zipcode_address="sample zip",
            state_address="sample state",
            creation_date='2006-08-21',
            modified_date='2006-08-22',
            description='Sample receipe description.',
            gender='Male',
            emergency_contact_name='Sample contact name',
            emergency_phone_number='+12345678',
            relationship='Father',
            is_in_hospital=True,
        )
        patients1.treatment.add(ing)
        patients2.treatment.add(ing)

        res = self.client.get(TREATMENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
