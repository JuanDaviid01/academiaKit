from django.db import models

# Create your models here.
class Institution(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    country = models.CharField(max_length=2, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"(self.name) ({self.code})"

class Campus(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.PROTECT, related_name="campuses")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    address = models.CharField(max_length=250)
    city = models.CharField(max_length=60)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["institution__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="uq_campus_institution_code"
            ),
            models.UniqueConstraint(
                fields=["institution", "name"], name="uq_campus_institution_name"
            ),
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
        ]

    def __str__(self):
        return f"{self.name} · {self.institution.code}"

class Building(models.Model):
    campus = models.ForeignKey(Campus, on_delete=models.PROTECT, related_name="buildings")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    floors = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ["campus__institution__name", "campus__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["campus", "code"], name="uq_building_campus_code"
            ),
            models.UniqueConstraint(
                fields=["campus", "name"], name="uq_building_campus_name"
            ),
        ]
        indexes = [
            models.Index(fields=["campus", "code"]),
        ]

    def __str__(self):
        return f"{self.name} · {self.campus.name}"
    
class Room(models.Model):
    class RoomType(models.TextChoices):
        CLASSROOM = "classroom", "Aula"
        LAB       = "lab",       "Laboratorio"
        OFFICE    = "office",    "Oficina"
        AUDITORIUM= "auditorium","Auditorio"
        VIRTUAL   = "virtual",   "Virtual"
    building = models.ForeignKey(Building, on_delete=models.PROTECT, related_name="Rooms")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, unique=True, db_index=True)
    capacity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = [
            "building__campus__institution__name",
            "building__campus__name",
            "building__name",
            "code",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["building", "code"], name="uq_room_building_code"
            ),
        ]
        indexes = [
            models.Index(fields=["building", "code"]),
        ]

    def __str__(self):
        b = self.building
        return f"{self.code} · {b.name} · {b.campus.name}"