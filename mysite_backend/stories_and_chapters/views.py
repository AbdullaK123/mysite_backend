from rest_framework import viewsets, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Story, Chapter
from django.core.exceptions import PermissionDenied
from .serializers import (
    StorySerializer,
    StoryDetailSerializer,
    ChapterSerializer,
    ChapterDetailSerializer
)


class StoryViewSet(viewsets.ModelViewSet):

    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer

    def perform_create(self, serializer):

        if not self.request.user.is_authenticated:

            raise PermissionDenied("Only authors can create stories")
        
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):

        object = self.get_object()

        if object.author != self.request.user:
            raise PermissionDenied("You are not the owner of this story")
        
        serializer.save()

    def perform_destroy(self, instance):

        if instance.author != self.request.user:
            raise PermissionDenied("You are not the owner of this story")
        
        instance.delete()

    @action(detail=True, methods=['get'])
    def full(self, request, pk=None):

        story = self.get_object()

        seralizer = StoryDetailSerializer(story)

        return Response(seralizer.data)

    @action(detail=True, methods=['post'])
    def add_chapter(self, request, pk=None):

        story = self.get_object()

        if not request.user.is_authenticated:
            return Response(
                {"detail": "You are not authenticated"},
                status=status.HTTP_403_FORBIDDEN
            )

        if story.author != request.user:
            return Response(
                {"detail": "You do not have permission to add chapters to this story."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ChapterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(story=story)
            return Response(
                serializer.data,
                status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST
            )



class ChapterViewSet(viewsets.ModelViewSet):

    queryset = Chapter.objects.all().order_by('created_at')
    serializer_class = ChapterSerializer

    @action(detail=True, methods=['get'])
    def full(self, request, pk=None):

        chapter = self.get_object()

        serializer = ChapterDetailSerializer(chapter)

        return Response(serializer.data)