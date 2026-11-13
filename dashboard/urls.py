from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="dashboard/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="home"), name="logout"),
    path("", views.overview, name="overview"),
    path("complaints/", views.complaint_list, name="complaints"),
    path(
        "complaints/<str:reference>/",
        views.complaint_detail,
        name="complaint_detail",
    ),
    path("feedback/", views.feedback_list, name="feedback"),
]
