from django.urls import path
from . import views

app_name = 'property_app'
urlpatterns = [
    path('', views.home, name='home'),
    path('', views.property_list, name='property-list'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile, name='profile'),
    path('update-email/', views.profile, name='update-email'),
    path('properties/', views.property_list, name='property_list'),
    path('properties/<int:id>/', views.property_detail, name='property-detail'),
    path('submit-maintenance-request/', views.submit_maintenance_request, name='submit_maintenance_request'),
    path('landlord-maintenance-requests/', views.landlord_maintenance_requests, name='landlord_maintenance_requests'),
    path('userhome/', views.user_registration_view, name='user-home'),
    path('user-dashboard/', views.user_dashboard, name='user-dashboard'),
    path('tenant-dashboard/', views.tenant_dashboard, name='tenant-dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('landlord-dashboard/', views.landlord_dashboard, name='landlord-dashboard'),
    path('payment/<int:property_id>/', views.payment_page, name='payment_page'),
]
