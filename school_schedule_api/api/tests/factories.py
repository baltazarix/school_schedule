import datetime

import factory

from api.models import SchoolClass, Teacher, Student, Subject, Schedule, DayOfWeekChoices


class StudentFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Student #{n}")
    school_class = factory.SubFactory("api.tests.factories.SchoolClassFactory")

    class Meta:
        model = Student


class SchoolClassFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"{n}A")

    class Meta:
        model = SchoolClass

    @factory.post_generation
    def students(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            self.students.add(*extracted)
        else:
            self.students.add(*[StudentFactory.create(school_class=self) for _ in range(3)])


class TeacherFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Teacher #{n}")

    class Meta:
        model = Teacher


class SubjectFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Subject #{n}")
    teacher = factory.SubFactory(TeacherFactory)

    class Meta:
        model = Subject


class ScheduleFactory(factory.django.DjangoModelFactory):
    school_class = factory.SubFactory(SchoolClassFactory)
    subject = factory.SubFactory(SubjectFactory)
    # generate day_of_week value against regular order
    day_of_week = factory.Sequence(lambda n: (len(DayOfWeekChoices) - 1) - (n % len(DayOfWeekChoices)))
    # generate a "round" hour values between 8 and 16 against regular order
    hour = factory.Sequence(lambda n: datetime.time(16 - (n % 9)))

    class Meta:
        model = Schedule
