from rest_framework import viewsets, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Story, Chapter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    StorySerializer,
    StoryDetailSerializer,
    ChapterSerializer,
    ChapterDetailSerializer
)


class StoryViewSet(viewsets.ModelViewSet):

    queryset = Story.objects.all().order_by('-created_at')
    serializer_class = StorySerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):

        queryset = Story.objects.all().order_by('-created_at')

        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(author_id = author_id)

        user = self.request.user
        if not user.is_authenticated or not user.is_staff:
            queryset = queryset.filter(is_published = True)

        return queryset


    @action(detail=True, methods=['get'])
    def full(self, request, pk=None):

        story = self.get_object()

        seralizer = StoryDetailSerializer(story)

        return Response(seralizer.data)

    @action(detail=True, methods=['post'])
    def add_chapter(self, request, pk=None):

        story = self.get_object()

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