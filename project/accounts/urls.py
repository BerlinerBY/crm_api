from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('user/employee/register/', views.reg_employee, name="reg_employee"),
    path('user/customer/register/', views.reg_customer, name="reg_customer"),
    path('user/employee/', views.get_employees, name="get_employees"),
    path('user/customer/', views.get_customers, name="get_customers"),
    path('user/', views.get_info, name="get_info"),
]