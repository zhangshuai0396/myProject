from django.urls import re_path

from good import views

urlpatterns = [
    re_path("operation/$", views.GoodsApiView.as_view()),
    re_path("operation/(?P<pk>\\d+)/$", views.SingleGoodApiView.as_view()),
    re_path("operation/list/", views.PageListGoodsApiView.as_view()),
    # re_path("operation/update/", views.SingleGoodUpdateApiView.as_view()),
]