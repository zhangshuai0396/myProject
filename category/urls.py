from django.urls import re_path

from category import views

urlpatterns = [
    re_path("operation/$", views.CategoryApiView.as_view()),
    re_path("operation/(?P<pk>\\d+)/$", views.SingleCategoryApiView.as_view()),
    re_path("operation/list/", views.PageListCategoryApiView.as_view()),
]