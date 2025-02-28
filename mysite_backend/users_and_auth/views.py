from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import action 
from rest_framework.response import Response 
from django.contrib.auth import get_user_model, authenticate, login, logout
from .serializers import UserSerializer, UserDetailSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):

        if self.action == 'create':

            permission_classes = [AllowAny]

        elif self.action in ['update', 'partial_update', 'delete']:

            permission_classes = [permissions.IsAuthenticated]

        else:

            permission_classes = [permissions.IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self):

        if self.action == 'retrieve':

            return UserDetailSerializer

        return UserSerializer
    

    @action(detail=False, methods=['get'])
    def me(self, request):

        serializer = UserDetailSerializer(request.user)

        return Response(serializer.data)
    


class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        print(f"Attempting login for: {username}")
        
        # Try to fetch the user directly
        try:
            user_obj = User.objects.get(username=username)
            print(f"User found: {user_obj}")
        except User.DoesNotExist:
            print("User does not exist")
        
        # Try authentication
        user = authenticate(username=username, password=password)
        print(f"Authentication result: {user}")
        
        if user:
            login(request, user)
            request.session.set_expiry(2592000)

            print(f"Session key: {request.session.session_key}")
            print(f"Session expiry: {request.session.get_expiry_date()}")
            print(f"Session data: {dict(request.session)}")


            return Response({'detail': 'login successful'})
        else:
            return Response(
                {'detail': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        print(f"Session key: {request.session.session_key}")
        print(f"Session expiry: {request.session.get_expiry_date()}")
        print(f"Session data: {dict(request.session)}")

        logout(request)
        
        return Response({'detail': 'logout successful'})