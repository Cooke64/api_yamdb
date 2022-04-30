from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.db import models

ROLE = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        'Имя пользователя', max_length=50, blank=False, unique=True)
    email = models.EmailField('Email', blank=False, unique=True,
                              validators=[validators.validate_email])
    bio = models.TextField('О себе', blank=True)
    confirmation_code = models.CharField('Код подтверждения', max_length=30,
                                         blank=True, null=True)
    role = models.CharField(
        'Права юзера', max_length=150, choices=ROLE, default='user')
    first_name = models.CharField(
        max_length=150, null=True, blank=True)
    last_name = models.CharField(
        max_length=150, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return True if not self.is_staff else None

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    def save(self, *args, **kwargs):
        if self.role == self.is_admin:
            self.is_staff = True
        super().save(*args, **kwargs)
