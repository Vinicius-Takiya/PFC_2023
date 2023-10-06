from django.urls import path, include
from .views import RoomView, UsersView, OrdersView, UserFilesView

urlpatterns = [
    path('room', RoomView.as_view()),
    path('users', UsersView.as_view()),
    path('userfiles', UserFilesView.as_view()),
    path('orders', OrdersView.as_view())
]
