from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("photoview", views.photoview, name="photoview"),
    #path("image", views.image, name="image"),
    path("useritemstore", views.create_user_item, name="createuser"),
    path('useritemshow', views.retrieve_user_items, name='user_items'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path(
        'accounts/login/',
        LoginView.as_view(template_name='login.html'),
        name='login'
    ),
]