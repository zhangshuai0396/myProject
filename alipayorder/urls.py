from django.urls import path

from alipayorder import views

urlpatterns = [
    path('order/pay/', views.OrderPayAPIView.as_view()),
    path('order/change/', views.OrderChangeAPIView.as_view())
]