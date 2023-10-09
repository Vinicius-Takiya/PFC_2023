from django.urls import path, include, re_path
from .views import get_csrf_token, send_registration_email, login, signup, test_token, UsersView, OrdersView, UserFilesView

urlpatterns = [
  re_path('send_email', send_registration_email),
  re_path('login', login),
  re_path('signup', signup),
  re_path('test_token', test_token),
  path('users', UsersView.as_view()),
  re_path('get_csrf_token', get_csrf_token),
  path('userfiles', UserFilesView.as_view()),
  path('orders', OrdersView.as_view()),
]
