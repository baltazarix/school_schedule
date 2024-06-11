from rest_framework.routers import SimpleRouter
from api.views.v1 import ScheduleListOnlyViewSet

v1_router = SimpleRouter()
v1_router.register(r"schedule", ScheduleListOnlyViewSet)
