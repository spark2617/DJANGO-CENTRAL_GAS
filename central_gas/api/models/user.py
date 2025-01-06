from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, telefone, password=None, **extra_fields):
        if not telefone:
            raise ValueError('O telefone é obrigatório')
        user = self.model(telefone=telefone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telefone, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(telefone, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    TIPO_CHOICES = (
        ('empresa', 'Empresa'),
        ('cliente', 'Cliente'),
    )
    telefone = models.CharField(max_length=15, null=True, blank=True, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    codigo_verificacao = models.CharField(max_length=5, null=True, blank=True)
    codigo_recuperacao = models.CharField(max_length=5, null=True, blank=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'telefone'
    REQUIRED_FIELDS = []  # Nenhum campo adicional obrigatório para criar um superusuário

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def __str__(self):
        return self.telefone
