from django.urls import path
from . import views
urlpatterns = [
 path('', views.dashboard, name='dashboard'),
 path('assets/', views.asset_list, name='asset_list'), path('assets/new/', views.asset_create, name='asset_create'),
 path('assets/<int:pk>/', views.asset_detail, name='asset_detail'), path('assets/<int:pk>/edit/', views.asset_edit, name='asset_edit'),
 path('assets/<int:pk>/delete/', views.asset_delete, name='asset_delete'), path('assets/<int:pk>/qr/', views.asset_qr, name='asset_qr'),
 path('scan/', views.scan, name='scan'), path('transactions/', views.transactions, name='transactions'),
 path('transactions/new/', views.transaction_create, name='transaction_create'), path('stocktake/', views.stocktake, name='stocktake'),
 path('reports/', views.reports, name='reports'), path('reports/export/', views.export_excel, name='export_excel'),
]
