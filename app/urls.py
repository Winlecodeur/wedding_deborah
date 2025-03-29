from django.urls import path
from . import views

urlpatterns = [

    #path for error page
    path('error/', views.error, name='error'),

    #path for scan qr 
    path('scan_qr/<int:invite_id>/', views.scan_qr, name='scan_qr'),
    path('scan/', views.scan, name='scan'),
    path('scan_error/<int:invite_id>/', views.scan_error, name='scan_error'),
    path('scan_invite/<int:invite_id>/', views.scan_invite, name='scan_invite'),
    #path for profile
    path('profile/', views.profile, name='profile'),

    #path for the main page, page of accueil
    path('<int:invite_id>/', views.home, name="home"),
    path('oath_home_form/<int:invite_id>/', views.oath_home_form, name='oath_home_form'),
    path('oath_home_delete/<int:invite_id>/<int:oath_id>/', views.oath_home_delete, name='oath_home_delete'),

    #path  for table 
    path('table/', views.table, name="table"),
    path('table_form/', views.table_form, name='table_form'),
    path('table_edit/<int:table_id>/', views.table_edit,name='table_edit'),
    path('table_detail/<int:table_id>/', views.table_detail,name='table_detail'),
    path('table_delete/<int:table_id>/', views.table_delete,name='table_delete'),
    path('table_search/', views.table_search,name='table_search'),

    #path for invite field 
    path('invite/', views.invite, name='invite'),
    path('invite_scan/', views.invite_scan, name='invite_scan'),
    path('invite_form/', views.invite_form, name='invite_form'),
    path('invite_search/', views.invite_search, name="invite_search"),
    path('invite_edit/<int:invite_id>', views.invite_edit, name='invite_edit'),
    path('invite_detail/<int:invite_id>', views.invite_detail, name='invite_detail'),
    path('invite_delete/<int:invite_id>', views.invite_delete, name='invite_delete'),

     #path for oath field 
    path('oath/', views.oath, name='oath'),
    path('oath_form/', views.oath_form, name='oath_form'),
    path('oath_search/', views.oath_search, name="oath_search"),
    path('oath_detail/<int:oath_id>/', views.oath_detail, name='oath_detail'),
    path('oath_delete/<int:oath_id>/', views.oath_delete, name='oath_delete'),
    path('oath_edit/<int:oath_id>/', views.oath_edit, name='oath_edit'),

    #path for logout
    path('logout_view/', views.logout_view, name="logout_view")


]