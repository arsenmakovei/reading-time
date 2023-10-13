from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from book.models import Book, ReadingSession
from book.serializers import (
    BookSerializer,
    BookListSerializer,
    BookDetailSerializer,
    ReadingSessionSerializer,
)


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer

        if self.action == "retrieve":
            return BookDetailSerializer

        if self.action in ("start_reading_session", "end_reading_session"):
            return ReadingSessionSerializer

        return BookSerializer

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def start_reading_session(self, request, pk=None):
        book = self.get_object()
        user = request.user

        active_session = ReadingSession.objects.filter(user=user, end_time=None).first()

        if active_session:
            if active_session.book == book:
                return Response(
                    {
                        "error": "You are already reading this book in an active session."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            active_session.end_time = timezone.now()
            active_session.save()

        ReadingSession.objects.create(user=user, book=book)

        return Response(
            {"message": f"Reading session for book '{book.title}' has started."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def end_reading_session(self, request, pk=None):
        book = self.get_object()
        user = request.user

        active_session = ReadingSession.objects.filter(
            user=user, book=book, end_time=None
        ).first()

        if active_session:
            active_session.end_time = timezone.now()
            active_session.save()

            return Response(
                {"message": f"Reading session for book '{book.title}' has ended."},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "No active reading session found for this book."},
            status=status.HTTP_400_BAD_REQUEST,
        )
