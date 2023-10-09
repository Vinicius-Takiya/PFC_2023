from django.urls import path, include, re_path
from .views import get_csrf_token, send_registration_email, create_user, UsersView, OrdersView, UserFilesView

urlpatterns = [
  re_path('send_email', send_registration_email),
  path('users', UsersView.as_view()),
  re_path('create_user', create_user),
  re_path('get_csrf_token', get_csrf_token),
  path('userfiles', UserFilesView.as_view()),
  path('orders', OrdersView.as_view()),
]
