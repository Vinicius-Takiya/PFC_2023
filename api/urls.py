from django.urls import path, include, re_path
from .views import get_csrf_token, send_registration_email, create_user, login, base_operators, operators,create_order, get_orders, get_orders_by_order_id, get_file, update_order_status,delete_order, UsersView, OrdersView, UploadedFileView

urlpatterns = [
  re_path('send_email', send_registration_email),
  path('users', UsersView.as_view()),
  re_path('create_user', create_user),
  re_path('login', login),  
  re_path('create_order', create_order),
  path('get_orders/<int:id>/', get_orders),
  path('delete_order/<int:order_id>/', delete_order),
  path('get_orders_by_order_id/<int:order_id>/', get_orders_by_order_id), 
  path('update_order_status/<int:order_id>/', update_order_status),  
  path('get_file/<int:id>/', get_file),
  re_path('base_operators', base_operators),
  re_path('operators', operators),
  re_path('get_csrf_token', get_csrf_token),
  path('userfiles', UploadedFileView.as_view()),
  path('orders', OrdersView.as_view()),
  path('files', UploadedFileView.as_view()),
]
