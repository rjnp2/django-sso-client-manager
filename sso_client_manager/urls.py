from django.urls import path

from .views import login, logout, profile, SetCodeView, login_checker

urlpatterns = [
    path('admin/login/', login, name='login'),
    path('admin/logout/', logout, name='logout'),
    path('profile/', profile),
    path('login-checker/', login_checker),
    path('set-code/', SetCodeView.as_view(), name='set-code'),
]
