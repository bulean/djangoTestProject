from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.index, name='index'),
    path('moveMoney', views.move_money, name='moveMoney'),
    path('getAccounts', views.get_all_accounts, name='getAccountsList'),
    path('getAccountsByInn/<int:inn>/', views.get_accounts_by_inn, name='getAccountsByInn'),
]
