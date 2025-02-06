from django.urls import path,include
from rango import views

app_name = 'rango'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('rango/', include('rango.urls')),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
]