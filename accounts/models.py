import uuid
import ssl
import geopy.geocoders
from .service import fill_city_with_alternative, generate_unique_incident_id
from django.db import models
from django.dispatch import receiver
from geopy.geocoders import Nominatim
from django.db.models.signals import pre_save
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from .constants import REPORT_CHOICES, PRIORITY_CHOICES, STATUS_CHOICES


# Disable SSL verification (not recommended for production)
geopy.geocoders.options.default_ssl_context = ssl._create_unverified_context()


class AccountManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, phone_number, password, **kwargs):
        user = self.model(phone_number=phone_number, is_staff=True, is_superuser=True, is_admin=True, **kwargs)
        user.password = make_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(unique=True, max_length=20)
    address = models.CharField(max_length=200)
    pin_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    class Meta:
        db_table = 'User'
        indexes = [
            models.Index(fields=[
                'email'
            ])
        ]

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.name

@receiver(pre_save, sender=User)
def get_city_country(sender, instance, **kwargs):

    if instance.pin_code:
        geolocator = Nominatim(user_agent="geoapiExercises")

        zipcode = instance.pin_code

        location = geolocator.geocode(query=zipcode, exactly_one=True, addressdetails=True, language="en")

        if location:
            address = location.raw["address"]
            city = fill_city_with_alternative(address).get("city", "")
            country = address.get("country", "")

        instance.city = city
        instance.country = country
        return instance.city, instance.country


class Incident(models.Model):
    id = models.CharField(primary_key=True, max_length=20, default=0)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(choices=REPORT_CHOICES, max_length=20)
    incident_details = models.TextField()
    reported_date_time = models.DateTimeField(auto_now_add=True)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20)

    def __str__(self):
        return self.id

@receiver(pre_save, sender=Incident)
def get_incident_id(sender, instance, **kwargs):
    if instance:
        instance.id = generate_unique_incident_id()
    if instance.status == 'Closed':
        raise ValueError("Cannot edit a closed Incident.")
    return instance.id



