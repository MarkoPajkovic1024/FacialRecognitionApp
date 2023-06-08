"""
Tests for models.
"""
from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create a return a new user."""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_patients(self):
        """Test creating a patients is successful."""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        patients = models.Patients.objects.create(
            user=user,
            first_name='Sample patients name',
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

        self.assertEqual(str(patients), patients.first_name)

    def test_create_tag(self):
        """Test creating a tag is successful."""
        user = create_user()
        tag = models.Tag.objects.create(user=user, name='Tag1')

        self.assertEqual(str(tag), tag.name)

    def test_create_treatment(self):
        """Test creating an ingredient is successful."""
        user = create_user()
        treatment = models.Treatment.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(treatment), treatment.name)

    @patch('core.models.uuid.uuid4')
    def test_patient_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.patients_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/patients/{uuid}.jpg')
