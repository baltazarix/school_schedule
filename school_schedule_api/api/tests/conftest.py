import pytest


@pytest.fixture(scope="function", autouse=True)
def drf_client():
    from rest_framework.test import APIClient

    yield APIClient()
