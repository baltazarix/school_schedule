from django.utils import timezone

from django_filters import rest_framework as filters

from api.models import Schedule


class ScheduleFilter(filters.FilterSet):
    class_name = filters.CharFilter(field_name="school_class__name", lookup_expr="iexact")
    for_today = filters.BooleanFilter(field_name="day_of_week", method="for_today_filter")

    def for_today_filter(self, queryset, name, value):
        if value:
            return queryset.filter(day_of_week=timezone.now().weekday())
        return queryset

    class Meta:
        model = Schedule
        fields = ["class_name", "for_today"]
