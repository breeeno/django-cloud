from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import AccessToken
from .models import User
from .serializers import UsersSerializers
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView 
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend



class RegisterUserView(generics.CreateAPIView):
    serializer_class = UsersSerializers
    permission_classes = [permissions.AllowAny]

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsersSerializers(request.user)
        return Response(serializer.data)

    def put(self, request):
        print(request.data)
        if request.data['password']:
            return Response({"error": "Password not expected."}, status=400)
        serializer = UsersSerializers(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        request.user.delete()
        return Response(status=204)
    
class UserList(ListAPIView):
    queryset = User.objects.all().order_by('name')
    serializer_class = UsersSerializers
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email', 'age']
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@api_view(['POST'])
def login_user(request):
    """Login an existing user. Email and password required."""
    email = request.data.get('email')
    password = request.data.get('password')
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)
    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):
            token = AccessToken.for_user(user)
            return Response({
                'message': 'Login successful',
                'access_token': str(token),
            }, status=200)
        else:
            return Response({'error': 'Invalid credentials'}, status=403)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=403)
    except Exception:
        return Response({'error': 'An error occurred during login'}, status=500)