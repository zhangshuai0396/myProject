from django.urls import re_path

from goodcar import views

urlpatterns = [
    re_path("operation/$", views.GoodCarApiView.as_view()),
    re_path("operation/(?P<pk>\\d+)/$", views.SingleGoodCarApiView.as_view()),
    re_path("operation/list/", views.PageListGoodCarApiView.as_view()),
]