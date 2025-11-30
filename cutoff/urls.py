from django.urls import path
from . import views

app_name = 'cutoff'

urlpatterns = [
    # Root
    path('', views.index_view, name='index'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Admin - PDF Upload (moved out of /admin/ to avoid conflict)
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('upload-pyq/', views.upload_pyq, name='upload_pyq'),
    
    # Cutoff Search
    path('cutoff-search/', views.cutoff_search, name='cutoff_search'),
    
    # API Endpoints
    path('api/get-branches/', views.api_get_branches, name='api_get_branches'),
    path('api/get-categories/', views.api_get_categories, name='api_get_categories'),
    
    # PYQ Management
    path('pyqs/', views.pyq_list, name='pyq_list'),
    path('pyqs/<int:pyq_id>/download/', views.pyq_download, name='pyq_download'),
]
