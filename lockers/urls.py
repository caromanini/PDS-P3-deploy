from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('locker/<int:locker_id>/change_password/', views.change_password, name='change_password'),
    path('locker/<int:locker_id>/change_owner_email/', views.change_owner_email, name='change_owner_email'),
]