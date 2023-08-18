from django.db import models
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
  def create_user(self, email, password=None, **extrafields):
    if not email:
      raise ValueError("Users must have an email address")
    user = self.model(email=self.normalize_email(email), **extrafields)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_superuser(self, email, password=None, **extrafields):
    user = self.create_user(email, password=password, **extrafields)
    user.is_admin = True
    user.save(using=self._db)
    return user


USER_TYPE = (
  ('', 'Select User Type'), 
  ('Doctor', 'Doctor'), 
  ('Patient', 'Patient'),
)
   
STATES = (
  ('', 'Select State'),
  ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands'),
  ('Andhra Pradesh', 'Andhra Pradesh'),
  ('Arunachal Pradesh', 'Arunachal Pradesh'),
  ('Assam', 'Assam'),
  ('Bihar', 'Bihar'),
  ('Chandigarh', 'Chandigarh'),
  ('Chhatisgarh', 'Chhatisgarh'),
  ('Dadra & Nagar Haveli', 'Dadra & Nagar Haveli'),
  ('Daman & Diu', 'Daman & Diu'),
  ('Delhi', 'Delhi'),
  ('Goa', 'Goa'),
  ('Gujarat', 'Gujarat'),
  ('Haryana', 'Haryana'),
  ('Himachal Pradesh', 'Himachal Pradesh'),
  ('Jammu & Kashmir', 'Jammu & Kashmir'),
  ('Jharkhand', 'Jharkhand'),
  ('Karnataka', 'Karnataka'),
  ('Kerala', 'Kerala'),
  ('Lakshadweep', 'Lakshadweep'),
  ('Madhya Pradesh', 'Madhya Pradesh'),
  ('Maharashtra', 'Maharashtra'),
  ('Manipur', 'Manipur'),
  ('Meghalaya', 'Meghalaya'),
  ('Mizoram', 'Mizoram'),
  ('Nagaland', 'Nagaland'),
  ('Odisha', 'Odisha'),
  ('Puducherry', 'Puducherry'),
  ('Punjab', 'Punjab'),
  ('Rajasthan', 'Rajasthan'),
  ('Sikkim', 'Sikkim'),
  ('Tamil Nadu', 'Tamil Nadu'),
  ('Telangana', 'Telangana'),
  ('Uttrakhand', 'Uttrakhand'),
  ('Uttar Pradesh', 'Uttar Pradesh'),
  ('West Bengal', 'West Bengal'), 
)

def pincode_validate(value):
  if value > 100000 and value < 999999:
    return value
  raise ValidationError("Pin Code is not valid")

class User(AbstractBaseUser):
  email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
  username = models.CharField(max_length=100, unique=True)
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  user_type = models.CharField(choices=USER_TYPE, max_length=100)
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  address = models.CharField(max_length=255, verbose_name="Address line 1")
  city = models.CharField(max_length=100)
  state = models.CharField(choices=STATES, max_length=100)
  pincode = models.PositiveIntegerField(validators=[pincode_validate])
  profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True,)

  objects = UserManager()

  USERNAME_FIELD = "email"
  REQUIRED_FIELDS = ["username", "pincode"]

  def __str__(self):
    return self.username

  def has_perm(self, perm, obj=None):
    "Does the user have a specific permission?"
    # Simplest possible answer: Yes, always
    return True

  def has_module_perms(self, app_label):
    "Does the user have permissions to view the app `app_label`?"
    # Simplest possible answer: Yes, always
    return True
  
  def get_full_name(self) -> str:
    return self.username

  @property
  def is_staff(self):
    "Is the user a member of staff?"
    # Simplest possible answer: All admins are staff
    return self.is_admin
  