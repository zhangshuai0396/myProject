from django.urls import re_path

from order import views

urlpatterns = [
    re_path("operation/$", views.CreateOrderAPIView.as_view()),
    re_path("operation/(?P<pk>\\d+)/$", views.SingleOrderApiView.as_view()),
    re_path("operation/list/", views.PageListOrderApiView.as_view()),
]