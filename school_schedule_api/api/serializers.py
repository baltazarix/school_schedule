from rest_framework import serializers

from api.models import Schedule, Subject, Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name",)
        model = Teacher


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ("name",)
        model = Subject


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Supposed to be used on a queryset with following annotation: ".annotate(student_count=Count("school_class__students"))"
    Thanks to that there is no n+1 for data returned at "class.student_count" path,
    and data serialization for queryset.count() > 1 will always result with a single database query.

    Another approach could be storing "student_count" directly on SchoolClass model.
    """

    subject = SubjectSerializer(read_only=True)
    teacher = TeacherSerializer(source="subject.teacher", read_only=True)

    def get_class(self, obj):
        return {
            "name": obj.school_class.name,
            "student_count": obj.student_count,
        }

    class Meta:
        fields = (
            "class",
            "subject",
            "day_of_week",
            "hour",
            "teacher",
        )
        model = Schedule


# a workaround needed to be done in order to achieve "class" key in the response
ScheduleSerializer._declared_fields["class"] = serializers.SerializerMethodField(read_only=True)
