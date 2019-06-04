from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.user_type = User.ADMIN
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    ADMIN = 1
    COMPANY = 2
    EMPLOYEE = 3
    USER_TYPE_CHOICES = [
        (ADMIN, 'Admin'),
        (COMPANY, 'Company'),
        (EMPLOYEE, 'Employee'),
    ]
    name = models.CharField(
        verbose_name='name or company name',
        max_length=100,
        blank=True, null=True
    )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_type = models.PositiveSmallIntegerField(
        choices=USER_TYPE_CHOICES,
        default=COMPANY,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_by = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_company(self):
        return self.user_type == self.COMPANY

    @property
    def is_employee(self):
        return self.user_type == self.EMPLOYEE

    @property
    def is_staff(self):
        return self.is_admin


class Invite(models.Model):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    token = models.SlugField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)