from django.urls import path
from .views import delete_worker, update_worker, worker_list, worker_detail, register, login

urlpatterns = [
    path('workers/', worker_list, name='worker-list'), 
    path('workers/<int:pk>/', worker_detail, name='worker-detail'),
    path('workers/<int:pk>/update/', update_worker, name='worker-update'),
    path('workers/<int:pk>/delete/', delete_worker, name='worker-delete'),

    path('register/', register, name='register'),
    path('login/', login, name='login'),

]
