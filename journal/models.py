from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    name = models.CharField(max_length=100, verbose_name="Предмет")

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    name = models.CharField(max_length=10, blank=True, null=True)
    grade_level = models.IntegerField()
    letter = models.CharField(max_length=1)

    @property
    def full_name(self):
        if self.name is None or self.name == "":
            return f"{self.grade_level}{self.letter}"

        return f"{self.name}({self.grade_level}{self.letter})"

    class Meta:
        verbose_name = "Класс"
        verbose_name_plural = "Классы"

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school_class = models.ForeignKey(
        SchoolClass, on_delete=models.CASCADE, verbose_name="Класс"
    )

    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def __str__(self):
        return self.full_name


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    children = models.ManyToManyField(
        Student, related_name="parents", verbose_name="Дети"
    )

    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject, verbose_name="Предметы")

    @property
    def full_name(self):
        return f"{self.user.last_name} {self.user.first_name}"

    def __str__(self):
        return self.full_name


class Grade(models.Model):
    VALUE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name="Ученик",
        related_name="grades",
    )
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, verbose_name="Предмет"
    )
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, verbose_name="Учитель"
    )
    value = models.IntegerField(choices=VALUE_CHOICES, verbose_name="Оценка")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    comment = models.TextField(verbose_name="Комментарий", blank=True)

    def __str__(self):
        return f"{self.student} — {self.subject}: {self.value}"
