from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path(
        'purchase_history/<uuid:purchase_id>/',
        views.purchase_history_detail,
        name='purchase_history_detail',
    ),
]