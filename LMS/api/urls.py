from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views
from api import views as a_views

# Initialize the router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'books', a_views.BookViewSet, basename='book')
router.register(r'book/info', a_views.BookInfoViewSet, basename='bookinfo')
router.register(r'checkout', a_views.CheckOutViewSet, basename='checkout')
router.register(r'history', a_views.TransactionHistoryViewSet, basename='history')

urlpatterns = [
    # API routes from the router
    path('', include(router.urls)),

    # Standalone API endpoints
    path('endpoints/', a_views.endpoints, name='endpoints'),

    # Authentication routes
    path('auth/basic/', obtain_auth_token, name='basic_token'), 
    
    path('auth/jwt/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'), 
    path('auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),  # JWT token refresh

    # Custom book-related actions
    path('books/<int:pk>/return/', a_views.return_book, name='return_book'),
    path('books/<int:pk>/checkout/', a_views.borrow_book, name='borrow_book'),
]
