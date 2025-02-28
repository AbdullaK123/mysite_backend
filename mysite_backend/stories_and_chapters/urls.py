from rest_framework.routers import DefaultRouter
from .views import StoryViewSet, ChapterViewSet


router = DefaultRouter()

router.register(r'stories', StoryViewSet)
router.register(r'chapters', ChapterViewSet)

urlpatterns = router.urls