from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class GenderTypes(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(correo_electronico=email, **extra_fields)
        user.set_password(password) # password encryption method
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    # defining sqlENUM
    class UserType(models.TextChoices):
        MEDIC = 'MEDIC', 'Medic'
        PATIENTS = 'PATIENT', 'Patient'
        ADMIN = 'ADMIN', 'Administrator'

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=UserType.choices)
    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' # making login via Email
    REQUIRED_FIELDS = ['user_type']

    class Meta:
        db_table = 'others' # enforcing sql table name

class Specialities(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    name = models.TextField(max_length=100, null=False, unique=True)
    description = models.TextField(max_length=100)
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'specialties'


class Medics(models.Model):
    class StatusType(models.TextChoices):
        ACTIVE = 'active', 'Active'
        LEAVE = 'leave', 'On leave'
        VACATION = 'vacation', 'On vacation'
        SUSPENDED = 'suspended', 'Suspended'
        TEMPORARY_LEAVE = 'temporary_leave', 'Temporary leave'
        PERMANENT_LEAVE = 'permanent_leave', 'Permanent leave'
        RETIRED = 'retired', 'Retired'
        CONTRACT_ENDED = 'contract_end', 'Contract ended'
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medic_profile')
    center_id = models.ManyToManyField('appointments.Center', related_name='medics',
                                       db_table='medics_center',
                                       null=False)
    specialty = models.ManyToManyField(Specialities, through='MedicSpeciality',)
    last_name = models.TextField(max_length=100)
    name = models.TextField(max_length=100)
    nic = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GenderTypes.gender_choices)
    phone_number = models.CharField(max_length=11)
    estado = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.ACTIVE,
        verbose_name="Current Status"
    )
    class Meta:
        db_table = 'medics'

class MedicSpecialties(models.Model):
    medic_id = models.ForeignKey(Medics, on_delete=models.CASCADE)
    speciality_id = models.ForeignKey(Specialities, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    description = models.TextField(max_length=100)
    class Meta:
        db_table = 'medic_specialties'
        unique_together = ('medics', 'specialties')
class Patients(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    nic = models.CharField(max_length=15)
    name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    gender = models.CharField(max_length=10, choices=GenderTypes.gender_choices)
    phone_number = models.CharField(max_length=11)
    birth_date = models.DateField()
    class Meta:
        db_table = 'patients'

