"""
Tests for patients APIs.
"""
import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import (
    Patients,
    Tag,
    Treatment,
)

from patients.serializers import (
    PatientsSerializer,
    PatientsDetailSerializer,
)

PATIENTS_URL = reverse('patients:patients-list')


def detail_url(patients_id):
    """Create and return a patients detail URL."""
    return reverse('patients:patients-detail', args=[patients_id])


def image_upload_url(patients_id):
    """Create and return an image upload URL."""
    return reverse('patients:patients-upload-image', args=[patients_id])


def create_patients(user, **params):
    """Create and return a sample patients."""
    defaults = {

        'first_name': 'Sample patients first_name',
        'last_name': 'Sample patients last_name',
        'med_list': 'sample med list',
        'age': 22,
        'phone_number': '+12345667',
        'date_of_birth': '2006-08-21',
        'street_address':  "sample address",
        'city_address': "sample city",
        'zipcode_address': "sample zip",
        'state_address': "sample state",
        'description': 'Sample description',
        'creation_date': '2006-08-21',
        'modified_date': '2006-08-21',
        'gender': 'Male',
        'emergency_contact_name': 'Sample contact name',
        'emergency_phone_number': '+12345678',
        'relationship': 'Father',
        'is_in_hospital': True,
        'link': 'http://example.com/patients.pdf',

    }
    defaults.update(params)

    patients = Patients.objects.create(user=user, **defaults)

    return patients


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicPatientsAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(PATIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivatePatientsApiTests(TestCase):
    """Test authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com',
                                password='test123')
        self.client.force_authenticate(self.user)

    def test_retrieve_petients(self):
        """Test retrieving a list of petients."""
        create_patients(user=self.user)

        create_patients(user=self.user)

        res = self.client.get(PATIENTS_URL)

        petients = Patients.objects.all().order_by('-id')
        serializer = PatientsSerializer(petients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_patients_list_limited_to_user(self):
        """Test list of petients is limited to authenticated user."""
        other_user = create_user(email='other@example.com',
                                 password='test123')
        create_patients(user=other_user)

        create_patients(user=self.user)

        res = self.client.get(PATIENTS_URL)

        petients = Patients.objects.filter(user=self.user)
        serializer = PatientsSerializer(petients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_patients_detail(self):
        """Test get patients detail."""
        patients = create_patients(user=self.user)

        url = detail_url(patients.id)
        res = self.client.get(url)

        serializer = PatientsDetailSerializer(patients)
        self.assertEqual(res.data, serializer.data)

    def test_create_patients(self):
        """Test creating a patients."""
        payload = {

            'first_name': 'Sample patients',
            'last_name': 'Sample patients last name',
            'age': 30,

        }
        res = self.client.post(PATIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patients = Patients.objects.get(id=res.data['id'])
        for k, v in payload.items():

            self.assertEqual(getattr(patients, k), v)
        self.assertEqual(patients.user, self.user)

    def test_partial_update(self):
        """Test partial update of a patient."""
        original_link = 'https://example.com/patient.pdf'
        patient = create_patients(
            user=self.user,
            first_name='Sample patient name',
            link=original_link,
        )

        payload = {'first_name': 'New patient first name'}
        url = detail_url(patient.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.first_name, payload['first_name'])
        self.assertEqual(patient.link, original_link)
        self.assertEqual(patient.user, self.user)

    def test_full_update(self):
        """Test full update of patient."""
        patients = create_patients(
            user=self.user,
            first_name='Sample patient title',
            link='https://exmaple.com/patient.pdf',
            description='Sample patient description.',
            phone_number='+12345678',
            emergency_phone_number='+12345678',
        )
        print(patients.first_name)

        payload = {
            "first_name": "joe",
            "last_name": "jay",
            "age": 0,
            "med_list": "string",
            "phone_number": "+999999999",
            # "date_of_birth": "2022-09-12",
            "street_address": "string",
            "city_address": "string",
            "zipcode_address": "string",
            "state_address": "string",
            "link": "string",
            "emergency_contact_name": "string",
            "emergency_phone_number": "+123456789",
            "relationship": "Spouse",
            "gender": "Male",
            "is_in_hospital": True,
            "description": "string"

        }
        url = detail_url(patients.id)
        print(url)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        patients.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(patients, k), v)
        self.assertEqual(patients.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the patient user results in an error."""
        new_user = create_user(email='user2@example.com', password='test123')
        patients = create_patients(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(patients.id)
        self.client.patch(url, payload)

        patients.refresh_from_db()
        self.assertEqual(patients.user, self.user)

    def test_delete_patients(self):
        """Test deleting a patients successful."""
        patients = create_patients(user=self.user)

        url = detail_url(patients.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patients.objects.filter(id=patients.id).exists())

    def test_patients_other_users_patients_error(self):
        """Test trying to delete another users patientsgives error."""
        new_user = create_user(email='user2@example.com', password='test123')
        patients = create_patients(user=new_user)

        url = detail_url(patients.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Patients.objects.filter(id=patients.id).exists())

    def test_create_patients_with_new_tags(self):
        """Test creating a patients with new tags."""
        payload = {
            'first_name': 'Elen',
            'last_name': 'Jack',
            'age': 50,
            'tags': [{'name': 'bad'}, {'name': 'good'}],
        }
        res = self.client.post(PATIENTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patientss = Patients.objects.filter(user=self.user)
        self.assertEqual(patientss.count(), 1)
        patients = patientss[0]
        self.assertEqual(patients.tags.count(), 2)
        for tag in payload['tags']:
            exists = patients.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_patients_with_existing_tags(self):
        """Test creating a patients with existing tag."""
        tag_good = Tag.objects.create(user=self.user, name='good')
        payload = {
            'first_name': 'jim',
            'last_name': 'Sample patients last name',
            'age': 60,
            'tags': [{'name': 'good'}, {'name': 'Critical'}],
        }
        res = self.client.post(PATIENTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patientss = Patients.objects.filter(user=self.user)
        self.assertEqual(patientss.count(), 1)
        patients = patientss[0]
        self.assertEqual(patients.tags.count(), 2)
        self.assertIn(tag_good, patients.tags.all())
        for tag in payload['tags']:
            exists = patients.tags.filter(
                name=tag['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_tag_on_update(self):
        """Test create tag when updating a patients."""
        patients = create_patients(user=self.user)

        payload = {'tags': [{'name': 'Improving'}]}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_tag = Tag.objects.get(user=self.user, name='Improving')
        self.assertIn(new_tag, patients.tags.all())

    def test_update_patients_assign_tag(self):
        """Test assigning an existing tag when updating a patients."""
        tag_stable = Tag.objects.create(user=self.user, name='Stable')
        patients = create_patients(user=self.user)
        patients.tags.add(tag_stable)

        tag_Improving = Tag.objects.create(user=self.user, name='Improving')
        payload = {'tags': [{'name': 'Improving'}]}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(tag_Improving, patients.tags.all())
        self.assertNotIn(tag_stable, patients.tags.all())

    def test_clear_patients_tags(self):
        """Test clearing a patients tags."""
        tag = Tag.objects.create(user=self.user, name='Regressing')
        patients = create_patients(user=self.user)
        patients.tags.add(tag)

        payload = {'tags': []}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(patients.tags.count(), 0)

    def test_create_patients_with_new_Treatment(self):
        """Test creating a patients with new Treatment."""
        payload = {
            "first_name": "joe",
            "last_name": "jay",
            "age": 0,
            "med_list": "string",
            "phone_number": "+999999999",
            # "date_of_birth": "2022-09-12",
            "street_address": "string",
            "city_address": "string",
            "zipcode_address": "string",
            "state_address": "string",
            "link": "string",
            "emergency_contact_name": "string",
            "emergency_phone_number": "+123456789",
            "relationship": "Spouse",
            "gender": "Male",
            "is_in_hospital": True,
            "description": "string",
            "treatment": [{'name': 'Cauliflower'}, {'name': 'Salt'}],

        }
        res = self.client.post(PATIENTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patientss = Patients.objects.filter(user=self.user)
        self.assertEqual(patientss.count(), 1)
        patients = patientss[0]
        self.assertEqual(patients.treatment.count(), 2)
        for treatmen in payload['treatment']:
            exists = patients.treatment.filter(
                name=treatmen['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_patients_with_existing_treatment(self):
        """Test creating a new patients with existing treatment."""
        treatmen = Treatment.objects.create(user=self.user, name='Lemon')
        payload = {
            "first_name": "joe",
            "last_name": "jay",
            "age": 0,
            "med_list": "string",
            "phone_number": "+999999999",
            # "date_of_birth": "2022-09-12",
            "street_address": "string",
            "city_address": "string",
            "zipcode_address": "string",
            "state_address": "string",
            "link": "string",
            "emergency_contact_name": "string",
            "emergency_phone_number": "+123456789",
            "relationship": "Spouse",
            "gender": "Male",
            "is_in_hospital": True,
            "description": "string",
            'treatment': [{'name': 'Lemon'}, {'name': 'Fish Sauce'}],

        }
        res = self.client.post(PATIENTS_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        patientss = Patients.objects.filter(user=self.user)
        self.assertEqual(patientss.count(), 1)
        patients = patientss[0]
        self.assertEqual(patients.treatment.count(), 2)
        self.assertIn(treatmen, patients.treatment.all())
        for treatmen in payload['treatment']:
            exists = patients.treatment.filter(
                name=treatmen['name'],
                user=self.user,
            ).exists()
            self.assertTrue(exists)

    def test_create_treatment_on_update(self):
        """Test creating an treatment when updating a patients."""
        patients = create_patients(user=self.user)

        payload = {'treatment': [{'name': 'Limes'}]}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        new_treatment = Treatment.objects.get(user=self.user, name='Limes')
        self.assertIn(new_treatment, patients.treatment.all())

    def test_update_patients_assign_treatment(self):
        """Test assigning an existing treatment when updating a patients."""
        treatment1 = Treatment.objects.create(user=self.user, name='Pepper')
        patients = create_patients(user=self.user)
        patients.treatment.add(treatment1)

        treatment2 = Treatment.objects.create(user=self.user, name='Chili')
        payload = {'treatment': [{'name': 'Chili'}]}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(treatment2, patients.treatment.all())
        self.assertNotIn(treatment1, patients.treatment.all())

    def test_clear_patients_treatment(self):
        """Test clearing a patients treatment."""
        treatment = Treatment.objects.create(user=self.user, name='Garlic')
        patients = create_patients(user=self.user)
        patients.treatment.add(treatment)

        payload = {'treatment': []}
        url = detail_url(patients.id)
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(patients.treatment.count(), 0)

    def test_filter_by_tags(self):
        """Test filtering patients by tags."""
        r1 = create_patients(user=self.user, first_name='Thai Vegetable Curry')
        r2 = create_patients(user=self.user,
                             first_name='Aubergine with Tahini')
        tag1 = Tag.objects.create(user=self.user, name='Vegan')
        tag2 = Tag.objects.create(user=self.user, name='Vegetarian')
        r1.tags.add(tag1)
        r2.tags.add(tag2)
        r3 = create_patients(user=self.user, first_name='Fish and chips')

        params = {'tags': f'{tag1.id},{tag2.id}'}
        res = self.client.get(PATIENTS_URL, params)

        s1 = PatientsSerializer(r1)
        s2 = PatientsSerializer(r2)
        s3 = PatientsSerializer(r3)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)

    def test_filter_by_treatment(self):
        """Test filtering patients by treatment."""
        r1 = create_patients(user=self.user, first_name='Posh Beans on Toast')
        r2 = create_patients(user=self.user, first_name='Chicken Cacciatore')
        in1 = Treatment.objects.create(user=self.user, name='Feta Cheese')
        in2 = Treatment.objects.create(user=self.user, name='Chicken')
        r1.treatment.add(in1)
        r2.treatment.add(in2)
        r3 = create_patients(user=self.user, first_name='Red Lentil Daal')

        params = {'treatment': f'{in1.id},{in2.id}'}
        res = self.client.get(PATIENTS_URL, params)

        s1 = PatientsSerializer(r1)
        s2 = PatientsSerializer(r2)
        s3 = PatientsSerializer(r3)
        self.assertIn(s1.data, res.data)
        self.assertIn(s2.data, res.data)
        self.assertNotIn(s3.data, res.data)


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'password123',
        )
        self.client.force_authenticate(self.user)
        self.patients = create_patients(user=self.user)

    def tearDown(self):
        self.patients.image.delete()

    def test_upload_image(self):
        """Test uploading an image to a patients."""
        url = image_upload_url(self.patients.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            res = self.client.post(url, payload, format='multipart')

        self.patients.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.patients.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image."""
        url = image_upload_url(self.patients.id)
        payload = {'image': 'notanimage'}
        res = self.client.post(url, payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
