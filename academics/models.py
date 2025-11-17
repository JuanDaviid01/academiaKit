from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from orgs.models import Institution
from core.models import TimeStampedActiveModel

# periodo academico o ciclo escolar
class AcademicTerm(TimeStampedActiveModel):

    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, related_name="academic_terms"
    )
    name = models.CharField(max_length=120)
    code = models.CharField(max_length=20, db_index=True)  # ej. "2025-1"
    start_date = models.DateField()
    end_date   = models.DateField()
    class Meta:
        ordering = ["-start_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="uq_term_institution_code"
            )
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self):
        return f"{self.name} · {self.institution.code}"

# facultad o escuela dentro de una institucion
class Department(TimeStampedActiveModel):
    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, related_name="departments"
    )
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, db_index=True)

    class Meta:
        ordering = ["institution__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="uq_dept_institution_code"
            )
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
        ]

    def __str__(self):
        return f"{self.name} · {self.institution.code}"

# carrera o programa de estudios
class Program(TimeStampedActiveModel):

    class Level(models.TextChoices):
        UNDERGRAD = "undergrad", "Pregrado"
        GRAD      = "grad",      "Posgrado"
        OTHER     = "other",     "Otro"

    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, related_name="programs"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="programs", null=True, blank=True
    )
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, db_index=True)  # ej. "ING-SIS"
    level = models.CharField(max_length=20, choices=Level.choices, default=Level.UNDERGRAD)
    total_credits = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(400)], default=160
    )

    class Meta:
        ordering = ["institution__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="uq_program_institution_code"
            )
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
            models.Index(fields=["level"]),
        ]

    def __str__(self):
        return f"{self.name} · {self.institution.code}"
# asignatura o materia
class Subject(TimeStampedActiveModel):
    class Modality(models.TextChoices):
        IN_PERSON = "in_person", "Presencial"
        ONLINE    = "online",    "Virtual"
        HYBRID    = "hybrid",    "Híbrido"

    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, related_name="subjects"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="subjects", null=True, blank=True
    )
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20, db_index=True)
    credits = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(40)], default=3)
    hours_theory = models.PositiveIntegerField(default=2)
    hours_practice = models.PositiveIntegerField(default=1)
    modality = models.CharField(max_length=20, choices=Modality.choices, default=Modality.IN_PERSON)

    class Meta:
        ordering = ["institution__name", "code"]
        constraints = [
            models.UniqueConstraint(
                fields=["institution", "code"], name="uq_subject_institution_code"
            )
        ]
        indexes = [
            models.Index(fields=["institution", "code"]),
            models.Index(fields=["department", "code"]),
        ]

    def __str__(self):
        return f"{self.code} · {self.name}"

#relacion de prerequisitos entre asignaturas
class SubjectPrerequisite(models.Model):
    institution = models.ForeignKey(
        Institution, on_delete=models.PROTECT, related_name="subject_prerequisites"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="prerequisites"
    )
    prerequisite = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="is_prerequisite_of"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(subject=models.F("prerequisite")),
                name="ck_subject_prereq_not_self",
            ),
            models.UniqueConstraint(
                fields=["institution", "subject", "prerequisite"],
                name="uq_subject_prereq_unique",
            ),
        ]
        indexes = [
            models.Index(fields=["institution", "subject"]),
        ]

    def __str__(self):
        return f"{self.prerequisite.code} → {self.subject.code}"

# relacion de asignaturas dentro de un programa
class ProgramSubject(TimeStampedActiveModel):
    program = models.ForeignKey(
        Program, on_delete=models.PROTECT, related_name="program_subjects"
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.PROTECT, related_name="program_links"
    )
    semester_number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)], default=1
    )
    is_mandatory = models.BooleanField(default=True)

    class Meta:
        ordering = ["program__name", "semester_number", "subject__code"]
        constraints = [
            models.UniqueConstraint(
                fields=["program", "subject"], name="uq_program_subject_unique"
            ),
        ]
        indexes = [
            models.Index(fields=["program", "semester_number"]),
        ]

    def __str__(self):
        return f"{self.program.code} · {self.subject.code} (S{self.semester_number})"