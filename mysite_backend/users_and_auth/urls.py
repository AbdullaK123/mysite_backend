from rest_framework.routers import DefaultRouter
from .views import UserViewSet, LoginView, LogoutView
from django.urls import path, include


router = DefaultRouter()

router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout')
]
