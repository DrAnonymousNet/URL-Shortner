from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
import pytz
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        print(kwargs)

        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,**kwargs
        )
        user.staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
            """
            Creates and saves a staff user with the given email and password.
            """
            user = self.create_user(
                email,
                password=password,
            )
            user.staff = True
            user.save(using=self._db)
            return user


    def create_testuser(self, email, password, **kwargs):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,**kwargs
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')


        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )
        print(kwargs)

        user.set_password(password)
        
        user.save(using=self._db)
        return user




class UserAccount(AbstractBaseUser, PermissionsMixin):

    TIMEZONE = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    timezone = models.CharField(max_length=50, default="UTC", choices=TIMEZONE)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    objects = UserManager()

    REQUIRED_FIELDS = ["timezone"]
    USERNAME_FIELD = 'email'

    def _get_full_name(self):
        return f"{self.firstname} {self.lastname}"


    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    @property
    def full_name(self):
        return self._get_full_name
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin