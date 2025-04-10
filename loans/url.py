from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('apply-loan/', views.apply_loan, name='apply_loan'),
    path('loan-list/', views.loan_list, name='loan_list'),
    path('loan-detail/<int:loan_id>/', views.loan_detail, name='loan_detail'),
    path('approve-reject-loan/<int:loan_id>/', views.approve_or_reject_loan, name='approve_or_reject_loan'),
]