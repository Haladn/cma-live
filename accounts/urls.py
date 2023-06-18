from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('account',views.accountsettings, name='account'),
    path('user',views.userpage,name='user_page'),
    path('register',views.register, name="register"),
    path("login",views.loginpage,name="login"),
    path("logout",views.logoutuser, name="logout"),
    path("",views.home, name='home'),
    path('customer/<str:pk>/', views.customers, name='customer'),
    path('products', views.products,name='product'),
    path("order_form/<str:pk>/",views.createOrder, name='order_form'),
    path("update_order/<str:pk>/",views.Updateorder, name='update_order'),
    path("delete_order/<str:pk>/",views.Delete, name="delete"),
    
    path('password_reset',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),name='password_reset'),
    path('password_reset_done',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name="password_reset_complete"),
]