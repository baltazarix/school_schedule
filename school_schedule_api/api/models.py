from django.db import models
from django.db.models.functions import Lower


class NameAbstractModel(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    """
    Potential improvement: by adding `student_count` field we wouldn't have to do this on database when querying,
    but as a tradeoff we would have to keep data in sync (e.g. by using post_signal and recalculating this field
    whenever Student.school_class would have changed)

    That could lead to potential data inconsistencies.
    """

    name = models.CharField(max_length=4)

    class Meta:
        verbose_name = "school class"
        verbose_name_plural = "school classes"
        constraints = [
            models.UniqueConstraint(Lower("name").asc(), name="unique_school_class"),
        ]

    def __str__(self):
        return self.name


class DayOfWeekChoices(models.IntegerChoices):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Schedule(models.Model):
    school_class = models.ForeignKey("api.SchoolClass", on_delete=models.CASCADE, related_name="schedules")
    subject = models.ForeignKey("api.Subject", on_delete=models.CASCADE, related_name="schedules")
    day_of_week = models.PositiveSmallIntegerField(choices=DayOfWeekChoices)
    hour = models.TimeField()

    def __str__(self):
        return f"{self.school_class} - {self.subject} - {self.get_day_of_week_display()} - {self.hour}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["school_class", "subject", "day_of_week", "hour"], name="unique_schedule"),
        ]


class Student(NameAbstractModel):
    school_class = models.ForeignKey("api.SchoolClass", on_delete=models.CASCADE, related_name="students")


class Subject(NameAbstractModel):
    teacher = models.ForeignKey("api.Teacher", on_delete=models.CASCADE, related_name="subjects")

    def __str__(self):
        return f"{self.name} ({self.teacher})"


class Teacher(NameAbstractModel):
    pass
