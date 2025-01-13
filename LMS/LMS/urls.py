from django.contrib import admin
from django.urls import path, include
from api.urls import schema_view

urlpatterns = [
    # Admin site route
    path('admin/', admin.site.urls),

    # API routes
    path('api/', include('api.urls')),  # Includes all API endpoints defined in `api.urls`

    # Default DRF authentication login/logout views
    path('auth/', include('rest_framework.urls')),  

    path('', schema_view.with_ui('swagger', cache_timeout=0), 
name='schema-swagger-ui'), #added this to make the landing page the swagger ui
]


# handler404 = 'utils.views.error_404'
# handler500 = 'utils.views.error_500'
