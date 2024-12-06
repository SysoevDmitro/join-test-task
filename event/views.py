from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, generics, status, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import EventSerializer, EventRegistrationSerializer, EventRegistrationListSerializer
from .models import Event, EventRegistration
from .tasks import send_registration_email


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['location', 'date']
    search_fields = ['title', 'description']

    def update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({"error": "You are not the organizer of this event"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({"error": "You are not the organizer of this event"}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        if event.organizer != request.user:
            return Response({"error": "You are not the organizer of this event"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)


class EventRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        user = request.user
        event = get_object_or_404(Event, id=event_id)

        if event_id and Event.objects.filter(id=event_id).exists():
            if EventRegistration.objects.filter(event_id=event_id, user=user).exists():
                return Response({"error": "You are already already registered for this event"}, status=400)

            send_registration_email.delay(user.email, event.title)

            return super().post(request, *args, **kwargs)
        return Response({"error": "Event not found"}, status=404)


class EventRegistrationsListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRegistrationListSerializer

    def get_queryset(self):
        event_id = self.kwargs.get("event_id")
        return EventRegistration.objects.filter(event_id=event_id)


class EventRegistrationDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        event_id = kwargs.get("event_id")
        user = request.user

        if not Event.objects.filter(id=event_id).exists():
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        registration = EventRegistration.objects.filter(event_id=event_id, user=user).first()
        if not registration:
            return Response({"error": "You are not registered for this event"}, status=status.HTTP_400_BAD_REQUEST)

        registration.delete()
        return Response({"message": "Successfully unregistered from the event"}, status=status.HTTP_200_OK)
