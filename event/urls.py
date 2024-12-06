from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import EventViewSet, EventRegistrationView, EventRegistrationsListView, EventRegistrationDeleteView

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='events')


urlpatterns = [
    path('', include(router.urls)),
    path('register/', EventRegistrationView.as_view(), name='registration'),
    path('events/<int:event_id>/registrations/', EventRegistrationsListView.as_view(), name='event-registrations'),
    path('events/<int:event_id>/registrations/delete/', EventRegistrationDeleteView.as_view(), name='event-registrations-delete'),
]

app_name = 'event'
