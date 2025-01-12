from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  # Exposed under `auth/` for clarity
]


# handler404 = 'utils.views.error_404'
# handler500 = 'utils.views.error_500'
