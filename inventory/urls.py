# pyrefly: ignore [missing-import]
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.dashboard, name='dashboard'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/export/csv/', views.export_products_csv, name='export_products_csv'),
    path('products/export/xlsx/', views.export_products_xlsx, name='export_products_xlsx'),
    path('products/low-stock/', views.low_stock_alert, name='low_stock_alert'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/edit/', views.edit_product, name='edit_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),

    path('stock-in/', views.stock_in_list, name='stock_in_list'),
    path('stock-in/add/', views.stock_in_add, name='stock_in_add'),

    path('stock-out/', views.stock_out_list, name='stock_out_list'),
    path('stock-out/add/', views.stock_out_add, name='stock_out_add'),

    path('activity-log/', views.activity_log, name='activity_log'),

    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
]
