from django.contrib import admin
from django.urls import path
from django.urls.conf import include, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('api-auth/', include('rest_framework.urls'))
]
