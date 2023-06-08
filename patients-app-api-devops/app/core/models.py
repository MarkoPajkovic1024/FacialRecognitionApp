"""
Database models.
"""
import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
# from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
# from address.models import AddressField


def patients_image_file_path(instance, filename):
    """Generate file path for new patients image."""
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'patients', filename)


class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


GENDER_CHOICES = (

    ("Male", "Male"),
    ("Female", "Female"),
    ("Transgender", "Transgender"),
    ("Non-binary/non-conforming", "Non-binary/non-conforming"),
    ("Prefer not to respond", "Prefer not to respond"),
)


TITLE_CHOICES = (

    ("Doctor", "Doctor"),
    ("Nurse", "Nurse"),
    ("Physical Therapist", "Physical Therapist"),

)

RELATIONSHIP_CHOICES = (

    ("Spouse", "Spouse"),
    ("Mother", "Mother"),
    ("Father", "Father"),
    ("Children", "Children"),
    ("Friend", "Friend"),
    ("Not Applicable", "PNot Applicable"),
)


class Image_File(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    image = models.ImageField(null=True,upload_to=patients_image_file_path)

    
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)   
    last_name = models.CharField(max_length=255)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered "
                                 + "in the format:'+999999999'. Up" +
                                 "to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17, blank=True)
    # Validators should be a list
    # phoneNumber = PhoneNumberField
    # (unique = True, null = False, blank = False)
    # date_of_birth = models.DateField(max_length=8)
    street_address = models.CharField(max_length=255)
    city_address = models.CharField(max_length=255)
    zipcode_address = models.CharField(max_length=255)
    state_address = models.CharField(max_length=255)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    department_id = models.IntegerField()
    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        default='Prefer not to respond',
        )

    role = models.CharField(
        max_length=50,
        choices=TITLE_CHOICES,
        )
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def greet(self):
        if self.gender == "Male":
            return 'Mr. ' + self.last_name
        elif self.gender == "Female":
            return 'Ms. ' + self.last_name
        else:
            return self.last_name

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Patients(models.Model):
    """Patients object."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    # email = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    med_list = models.TextField(blank=True)
    age = models.IntegerField()
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')
    treatment = models.ManyToManyField('Treatment')
    image = models.ImageField(null=True, upload_to=patients_image_file_path)
    image_lists = models.ManyToManyField(Image_File,related_name = "image_lists")
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered "
                                 + "in the format:'+999999999'. Up" +
                                 "to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex],
                                    max_length=17, blank=True)
    date_of_birth = models.DateField(auto_now=False, null=True)
    street_address = models.CharField(max_length=255, blank=True)
    city_address = models.CharField(max_length=255, blank=True)
    zipcode_address = models.CharField(max_length=255, blank=True)
    state_address = models.CharField(max_length=255, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    modified_date = models.DateTimeField(auto_now=True, blank=True)
    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICES,
        default='Prefer not to respond',
        )

    emergency_contact_name = models.CharField(max_length=255, default="",
                                              blank=True)
    emergency_phone_number = models.CharField(validators=[phone_regex],
                                              max_length=17, blank=True)

    relationship = models.CharField(
        max_length=50,
        choices=RELATIONSHIP_CHOICES,
        default='Not Applicable',
        )

    is_in_hospital = models.BooleanField(default=True)

    def greet(self):
        if self.patient_gender == "Male":
            return 'Mr. ' + self.last_name
        elif self.patient_gender == "Female":
            return 'Ms. ' + self.last_name
        else:
            return self.last_name

    def __str__(self):
        return self.first_name


class Tag(models.Model):
    """Tag for filtering patients."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class Treatment(models.Model):
    """Treatments for patients."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

# # hereeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee
# class Patient(models.Model):
#     """patient object."""
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     title = models.CharField(max_length=255)
#     # firsttt_name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     time_minutes = models.IntegerField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     link = models.CharField(max_length=255, blank=True)

    # def __str__(self):
    #     return self.title

    # """patient object."""
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )

    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # # email = models.CharField(max_length=255)
    # description = models.TextField(blank=True)
    # # med_list = models.TextField(blank=True)
    # # age = models.IntegerField()
    # # link = models.CharField(max_length=255, blank=True)
    # # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
    # #                              message="Phone number must be entered "
    # #                              + "in the format:'+999999999'. Up" +
    # #                              "to 15 digits allowed.")
    # # phone_number = models.CharField(validators=[phone_regex],
    # #                                 max_length=17, blank=True)
    # # date_of_birth = models.DateField(auto_now=False, null=True)
    # # street_address = models.CharField(max_length=255, blank=True)
    # # city_address = models.CharField(max_length=255, blank=True)
    # # zipcode_address = models.CharField(max_length=255, blank=True)
    # # state_address = models.CharField(max_length=255, blank=True)
    # # creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    # # modified_date = models.DateTimeField(auto_now=True, blank=True)
    # # gender = models.CharField(
    # #     max_length=50,
    # #     choices=GENDER_CHOICES,
    # #     default='Prefer not to respond',
    # #     )

    # # emergency_contact_name = models.CharField(max_length=255, default="",
    # #                                           blank=True)
    # # emergency_phone_number = models.CharField(validators=[phone_regex],
    # #                                           max_length=17, blank=True)

    # # relationship = models.CharField(
    # #     max_length=50,
    # #     choices=RELATIONSHIP_CHOICES,
    # #     default='Not Applicable',
    # #     )

    # # is_in_hospital = models.BooleanField(default=True)

    # def greet(self):
    #     if self.patient_gender == "Male":
    #         return 'Mr. ' + self.last_name
    #     elif self.patient_gender == "Female":
    #         return 'Ms. ' + self.last_name
    #     else:
    #         return self.last_name

    # def __str__(self):
    #     return self.first_name
