from django.urls import path
from .views import LoginView, RegisterView, log_out

app_name = "users"


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("logout/", log_out, name="logout"),
]
