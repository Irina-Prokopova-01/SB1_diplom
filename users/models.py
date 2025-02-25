from django.contrib.auth.models import AbstractUser
from django.db import models


ROLE_CHOICES = (
    ("user", "User"),
    ("admin", "Admin"),
)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, help_text="Укажите вашу почту")
    first_name = models.CharField(
        max_length=30,
        help_text="Укажите ваше имя"
    )
    last_name = models.CharField(
        max_length=30,
        help_text="Укажите вашу фамилию"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Номер телефона",
        blank=True,
        null=True,
        help_text="Введите номер телефона",
    )
    image = models.ImageField(
        upload_to="users/image",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите изображение",
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
