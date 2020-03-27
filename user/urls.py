from django.urls import path, re_path

from user import views

urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("list/", views.UserListView.as_view()),
    path("detail/", views.UserDetailView.as_view())
]
