from django.urls import path
from . import views

app_name = 'catalogue'

urlpatterns = [
    path('', views.catalogue_view, name='catalogue'),
    path('download/<int:product_id>/', views.download_file, name='download_avatar'),
]

