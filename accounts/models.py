from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #Hereda: username, email, first_name, last_name, is_active, is_staff, is_superuser, last_login, date_joined, etc.
    class Roles(models.TextChoices):
        STUDENT = "student", "Estudiante"
        TEACHER = "teacher", "Docente"
        ADMIN   = "admin",   "Admin"
    # Campos extra mínimos del proyecto
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)
    document_id = models.CharField("Documento", max_length=50, blank=True, unique=True)
    phone = models.CharField(max_length=30, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} · {self.get_role_display()}"

    @property
    def is_student(self): return self.role == self.Roles.STUDENT
    @property
    def is_teacher(self): return self.role == self.Roles.TEACHER
    @property
    def is_admin(self):   return self.role == self.Roles.ADMIN