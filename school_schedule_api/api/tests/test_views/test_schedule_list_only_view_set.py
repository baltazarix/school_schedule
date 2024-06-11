import datetime
from unittest import mock

import pytest

from django.urls import reverse
from rest_framework import status

from api.models import DayOfWeekChoices
from api.tests.factories import ScheduleFactory, SchoolClassFactory

pytestmark = [pytest.mark.django_db]


class TestScheduleListOnlyViewSet:

    @mock.patch("api.filters.timezone")
    def test_for_today_true_filter_with_matching_schedule(self, mocked_timezone, drf_client):
        """
        ?/for_today=true should return schedules whose "day_of_week" matches value returned by timezone.now().weekday()
        """
        mocked_value = datetime.datetime(2024, 5, 16, tzinfo=datetime.timezone.utc)
        mocked_timezone.now.return_value = mocked_value
        ScheduleFactory(day_of_week=mocked_value.weekday())
        response = drf_client.get(reverse("api-v1:schedule-list") + "?for_today=true")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    @mock.patch("api.filters.timezone")
    def test_for_today_true_filter_without_matching_schedule(self, mocked_timezone, drf_client):
        """
        ?/for_today=true should return schedules whose "day_of_week" matches value returned by timezone.now().weekday()

        If there is no matching schedules, response should be empty
        """
        mocked_value = datetime.datetime(2024, 5, 16, tzinfo=datetime.timezone.utc)
        mocked_timezone.now.return_value = mocked_value
        ScheduleFactory(day_of_week=mocked_value.weekday() + 1)
        response = drf_client.get(reverse("api-v1:schedule-list") + "?for_today=true")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    @mock.patch("api.filters.timezone")
    def test_for_today_false_filter(self, mocked_timezone, drf_client):
        """
        ?/for_today=false should return all schedules
        """
        mocked_value = datetime.datetime(2024, 5, 16, tzinfo=datetime.timezone.utc)
        mocked_timezone.now.return_value = mocked_value
        schedules = [ScheduleFactory.create(day_of_week=x) for x in range(len(DayOfWeekChoices))]
        response = drf_client.get(reverse("api-v1:schedule-list") + "?for_today=false")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(schedules)

    @mock.patch("api.filters.timezone")
    def test_for_today_false_filter_not_specified(self, mocked_timezone, drf_client):
        """
        if ?/for_today is not specified, then it should defaults to "false" value and return all schedules
        """
        mocked_value = datetime.datetime(2024, 5, 16, tzinfo=datetime.timezone.utc)
        mocked_timezone.now.return_value = mocked_value
        schedules = [ScheduleFactory.create(day_of_week=x) for x in range(len(DayOfWeekChoices))]
        response = drf_client.get(reverse("api-v1:schedule-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == len(schedules)

    def test_class_name_filter_with_matching_results(self, drf_client):
        """
        ?/class_name=x should return all schedules whose Schedule.school_class.name == x
        """
        school_class_name = "3H"
        ScheduleFactory.create(school_class__name=school_class_name)
        response = drf_client.get(reverse("api-v1:schedule-list") + f"?class_name={school_class_name}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1

    def test_class_name_filter_without_matching_results(self, drf_client):
        """
        ?/class_name=x should return all schedules whose Schedule.school_class.name == x

        If there is no matching results, response should be empty
        """
        school_class_name = "3H"
        school_class = SchoolClassFactory.create(name=school_class_name)
        ScheduleFactory.create(school_class=school_class)
        response = drf_client.get(reverse("api-v1:schedule-list") + f"?class_name={school_class_name + 'a'}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 0

    def test_response_order(self, drf_client):
        """
        Response should be sorted by Schedule.day_of_week and Schedule.hour
        """
        fourth_schedule = ScheduleFactory.create(day_of_week=2, hour=datetime.time(hour=8), school_class__name="4A")
        third_schedule = ScheduleFactory.create(day_of_week=1, hour=datetime.time(hour=9), school_class__name="3A")
        second_schedule = ScheduleFactory.create(day_of_week=0, hour=datetime.time(hour=13), school_class__name="2A")
        first_schedule = ScheduleFactory.create(day_of_week=0, hour=datetime.time(hour=12), school_class__name="1A")
        response = drf_client.get(reverse("api-v1:schedule-list"))
        response_json = response.json()
        assert response_json[0]["class"]["name"] == first_schedule.school_class.name
        assert response_json[1]["class"]["name"] == second_schedule.school_class.name
        assert response_json[2]["class"]["name"] == third_schedule.school_class.name
        assert response_json[3]["class"]["name"] == fourth_schedule.school_class.name
