from django.db.models import Count

from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from api.filters import ScheduleFilter
from api.models import Schedule
from api.serializers import ScheduleSerializer


class ScheduleListOnlyViewSet(ListModelMixin, GenericViewSet):
    queryset = (
        Schedule.objects.select_related("school_class", "subject__teacher")
        .annotate(student_count=Count("school_class__students"))
        .order_by("day_of_week", "hour")
    )

    serializer_class = ScheduleSerializer
    permission_classes = [AllowAny]
    filterset_class = ScheduleFilter
