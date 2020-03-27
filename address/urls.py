from django.urls import path, re_path

from address import views

urlpatterns = [
    re_path("operation/$", views.AddressApiView.as_view()),
    re_path("operation/(?P<pk>\\d+)/$", views.SingleAddressApiView.as_view()),
    re_path("operation/list/", views.PageListAddressApiView.as_view()),
]