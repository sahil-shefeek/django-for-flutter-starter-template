import random
import string
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group,
)
from django.core.validators import EmailValidator
from django.db import models


class InterfaceUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, username=None):
        if not email:
            raise ValueError("User must have an email address")
        if not name:
            raise ValueError("User must have a name")

        if not username:
            # Generate a unique username from the email
            base_username = email.split("@")[0]
            username = self._generate_unique_username(base_username)

        user = self.model(
            email=self.normalize_email(email), name=name, username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(Group.objects.get(name="User"))
        user.save(using=self._db)
        return user

    def create_admin(self, email, name, password=None, username=None):
        user = self.create_user(email, name, password, username)
        user.groups.add(Group.objects.get(name="Admin"))
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, username=None):
        user = self.create_admin(email, name, password, username)
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def _generate_unique_username(self, base_username):
        # Append random digits to ensure uniqueness
        while True:
            random_suffix = "".join(random.choices(string.digits, k=4))
            username = f"{base_username}{random_suffix}"
            if not self.model.objects.filter(username=username).exists():
                return username


class InterfaceUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    name = models.CharField(max_length=125)
    objects = InterfaceUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        # For superusers
        if self.is_superuser:
            return True

        # Check if user belongs to admin group
        if self.is_admin:
            return True

        # For regular group permissions
        if "." in perm:
            app_label, codename = perm.split(".")
            return self.groups.filter(
                permissions__codename=codename,
                permissions__content_type__app_label=app_label,
            ).exists()

        return False

    def has_module_perms(self, app_label):
        # For superusers
        if self.is_superuser:
            return True

        # For admin group members
        if self.is_admin:
            return True

        # Check if user has any permissions for the app
        return self.groups.filter(
            permissions__content_type__app_label=app_label
        ).exists()

    @property
    def is_admin(self):
        return self.groups.filter(name="Admin").exists()

    @property
    def is_staff(self):
        return self.is_admin
