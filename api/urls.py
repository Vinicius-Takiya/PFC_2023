from django.urls import path, include, re_path
from .views import get_csrf_token, send_registration_email, create_user, login, get_authenticated_user, base_operators, create_order, UsersView, OrdersView, UploadedFileView

urlpatterns = [
  re_path('send_email', send_registration_email),
  path('users', UsersView.as_view()),
  re_path('create_user', create_user),
  re_path('login', login),  
  re_path('get_authenticated_user', get_authenticated_user),
  re_path('create_order', create_order),
  re_path('base_operators', base_operators),
  re_path('get_csrf_token', get_csrf_token),
  path('userfiles', UploadedFileView.as_view()),
  path('orders', OrdersView.as_view()),
]
