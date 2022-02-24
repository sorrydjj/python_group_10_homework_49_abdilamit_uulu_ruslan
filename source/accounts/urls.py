from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from accounts.views import login_view, logout_view, RegisterView, UserProfileView, UsersView, UpdateUserView, UserPasswordChangeView


app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name="login.html"), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="registration"),
    path("<int:pk>/", UserProfileView.as_view(), name="user_profile"),
    path("list", UsersView.as_view(), name="users_list"),
    path("update/", UpdateUserView.as_view(), name="user_update"),
    path("change-password/", UserPasswordChangeView.as_view(), name="change_password")

]