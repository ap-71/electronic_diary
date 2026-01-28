from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from journal import views

urlpatterns = [
    path("admin/", admin.site.urls, name="admin"),
    path("", views.home, name="home"),
    path("grades/", views.my_grades, name="my_grades"),
    path("grades/<int:grade_id>/", views.grade_detail, name="grade_detail"),
    path("add-grade/", views.add_grade, name="add_grade"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
