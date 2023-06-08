"""
Tests for the tags API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Tag,
    Patients,
)

from patients.serializers import TagSerializer


TAGS_URL = reverse('patients:tag-list')


def detail_url(tag_id):
    """Create and return a tag detail url."""
    return reverse('patients:tag-detail', args=[tag_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class PublicTagsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving tags."""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving a list of tags."""
        Tag.objects.create(user=self.user, name='urgent')
        Tag.objects.create(user=self.user, name='stable')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test list of tags is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Tag.objects.create(user=user2, name='critical')
        tag = Tag.objects.create(user=self.user, name='moderate')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
        self.assertEqual(res.data[0]['id'], tag.id)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(user=self.user, name='After Dinner')

        payload = {'name': 'good'}
        url = detail_url(tag.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, payload['name'])

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')

        url = detail_url(tag.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tags = Tag.objects.filter(user=self.user)
        self.assertFalse(tags.exists())

    def test_filter_tags_assigned_to_patients(self):
        """Test listing tags to those assigned to patients."""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        patients = Patients.objects.create(
            user=self.user,
            first_name='Green Eggs on Toast',
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
        patients.tags.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        s1 = TagSerializer(tag1)
        s2 = TagSerializer(tag2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)

    def test_filtered_tags_unique(self):
        """Test filtered tags returns a unique list."""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        Tag.objects.create(user=self.user, name='Dinner')
        patients1 = Patients.objects.create(
            user=self.user,
            first_name='Pancakes',
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
            first_name='Porridge',
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
        patients1.tags.add(tag)
        patients2.tags.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
