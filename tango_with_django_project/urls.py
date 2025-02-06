from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rango/', include('rango.urls')),
    path('', lambda request: HttpResponseRedirect('/rango/')),  # Redirect root to rango
]
