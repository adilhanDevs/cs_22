from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise TypeError("Users must have a username.")
        if password is None:
            raise TypeError("Users must have a password.")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class GenderChoice(models.Choices):
    male = 'male'
    female = 'female'


class Account(AbstractUser):
    name = models.CharField(max_length=255, verbose_name="Имя")
    age = models.IntegerField(default=0, verbose_name="Возраст")
    avatar = models.FileField(upload_to="avatar", blank=True, verbose_name="Аватар")
    gender = models.CharField(max_length=10, choices=GenderChoice.choices, verbose_name="Пол")
    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"


