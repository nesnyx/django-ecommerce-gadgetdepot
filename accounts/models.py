from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.



# This model use for us to create user or create super user
class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name,username,email,password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,first_name, last_name,username,email,password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        raise user
        

class Account(AbstractBaseUser):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=50)

    # Require
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login= models.DateTimeField(auto_now_add=True)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    # This code for change default require field username to email for user if wanna login later
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    # This objects to indicate to tell this function use My Account Manager for create user
    objects = MyAccountManager()

    def __str__(self) -> str:
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True




class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=200, blank=True)
    address_line_2 = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(blank=True,upload_to='photos//userprofile')
    city= models.CharField(blank=True, max_length=100)
    state= models.CharField(blank=True, max_length=100)
    country= models.CharField(blank=True, max_length=100)

    def __str__(self) -> str:
        return self.user.first_name
    
    def full_address(self):
        return f"{self.address_line_1} {self.address_line_2}"

