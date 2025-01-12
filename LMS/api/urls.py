from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views
from api import views as a_views

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Library Management System API",
      default_version='v1',
      description="An API to manage Books in a Library",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="cephas.tay137@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   
)



# Initialize the router and register viewsets
router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='users')
router.register(r'books', a_views.BookViewSet, basename='book')
router.register(r'booksinfo', a_views.BookInfoViewSet, basename='bookinfo')
router.register(r'checkout', a_views.CheckOutViewSet, basename='checkout')
router.register(r'checkout_history', a_views.TransactionHistoryViewSet, basename='history')

urlpatterns = [
    # API routes from the router
    path('', include(router.urls)),

    # Standalone API endpoints
    path('endpoints/', a_views.endpoints, name='endpoints'),

    # Token obtain routes
    path('token/basic/', obtain_auth_token, name='basic_token'), 
    
    path('token/jwt/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'), 
    path('token/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),  # JWT token refresh

    # Custom book-related actions
    path('books/<int:pk>/return/', a_views.return_book, name='return_book'),
    path('books/<int:pk>/checkout/', a_views.borrow_book, name='borrow_book'),

    #swagger docs
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
