from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, WishListItem
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, WishListItemSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render

# Create your views here.

class WishListItemViewSet(viewsets.ModelViewSet):
    serializer_class = WishListItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WishListItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'No tiene permiso para ver esta información.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)

class UserDetailView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'No tiene permiso para editar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        usuario = self.get_object()
        if usuario == request.user:
            return Response({'detail': 'No puede editarse a sí mismo.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().put(request, *args, **kwargs)

class UserDeactivateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            return Response({'detail': 'No tiene permiso para desactivar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        usuario = self.get_object()
        if usuario == request.user:
            return Response({'detail': 'No puede desactivarse a sí mismo.'}, status=status.HTTP_400_BAD_REQUEST)
        usuario.state = False
        usuario.save()
        return Response({'detail': 'Usuario desactivado exitosamente.'}, status=status.HTTP_200_OK)