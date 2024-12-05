from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from .serializers import EventSerializer, EventRegistrationSerializer
from .models import Event


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventSerializer


class EventRegistrationView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EventRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        event_id = request.data.get("event")
        if event_id and Event.objects.filter(id=event_id).exists():
            return super().post(request, *args, **kwargs)
        return Response({"error": "Event not found"}, status=404)
