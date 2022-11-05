from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("", views.index, name="index"),
    path("logout/", views.logout, name="logout"),
    path("delete/", views.delete, name="delete"),
    path("profile/password/", views.changePassword, name="changePassword"),
    path("<int:user_pk>/", views.detail, name="detail"),
    path("update/", views.update, name="update"),
    path("<int:user_pk>/follow/", views.follow, name="follow"),
    path("profile/<int:pk>/", views.profile, name="profile"),
]
