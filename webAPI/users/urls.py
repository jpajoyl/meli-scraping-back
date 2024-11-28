from django.urls import path, include
from .views import RegisterView, LoginView, UserListView, UserDetailView, UserDeactivateView, WishListItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'wishlist', WishListItemViewSet, basename='wishlist')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', UserListView.as_view(), name='usuarios'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='usuario_detalle'),
    path('users/<int:pk>/disable/', UserDeactivateView.as_view(), name='usuario_desactivar'),
    path('', include(router.urls)),
]