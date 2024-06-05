from django.urls import path
from . import views
from .views import product_list, add_to_cart

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('password_reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('product_list/', views.product_list, name='product_list'),
    path('add/', views.add_product, name='add_product'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_product/<int:product_id>/', views.remove_product, name='remove_product'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_logs/', views.view_logs, name='view_logs'),
    path('payment_process/', views.payment_process, name='payment_process'),

]

