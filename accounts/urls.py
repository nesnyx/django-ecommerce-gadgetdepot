from django.urls import path
from accounts import views
urlpatterns = [
    path('register/',view=views.register,name='register_page'),
    path('login/',view=views.login,name='login_page'),
    path('logout/',view=views.logout,name='logout'),
    path('dashboard/',view=views.dashboard,name='dashboard_page'),
    path('',view=views.dashboard,name='dashboard_page'),
    path('forgetPassword/', view=views.forgetPassword, name='forgetPassword'),
    path("activate/<uidb64>/<token>",view=views.activate, name='activate'),
    path("resetpassword/<uidb64>/<token>",view=views.resetPassword_validate, name='reset_password_validator'),
    path("resetPassword/",view=views.resetPassword, name='resetPassword'),
    path('my_orders/',view=views.my_orders, name='my_orders'),
    path('edit_profile/', view=views.edit_profile, name='edit_profile'),
    path('order_detail/<int:order_id>', view=views.order_detail,name='order_detail_dashboard')
]
