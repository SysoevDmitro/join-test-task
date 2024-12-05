from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, EventRegistrationView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', EventRegistrationView.as_view(), name='registration')
]

app_name = 'event'
