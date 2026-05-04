from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from sks import views
from django.contrib.auth.views import LogoutView
from sks.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    # Static Pages
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_service, name='terms'),
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/<slug:slug>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<slug:slug>/apply/', views.apply_for_job, name='apply_for_job'),
    
    # Blog URLs
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    
    # Case Study URLs
    path('case-studies/', views.CaseStudyListView.as_view(), name='case_study_list'),
    path('case-studies/<slug:slug>/', views.CaseStudyDetailView.as_view(), name='case_study_detail'),
    
    # Resource URLs
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    
    # Contact URLs
    path('contact/', views.contact_view, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    
    # Admin URLs (CRUD Operations)
    # Job CRUD
    path('admin/jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('admin/jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('admin/jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    
    # Applicant CRUD
    path('admin/applicants/', views.applicant_list, name='applicant_list'),
    path('admin/applicants/<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('admin/applicants/<int:pk>/edit/', views.applicant_update, name='applicant_update'),
    path('admin/applicants/<int:pk>/delete/', views.applicant_delete, name='applicant_delete'),
    
    # Employer Lead CRUD
    path('admin/leads/', views.employer_lead_list, name='employer_lead_list'),
    path('admin/leads/<int:pk>/', views.employer_lead_detail, name='employer_lead_detail'),
    path('admin/leads/create/', views.employer_lead_create, name='employer_lead_create'),
    path('admin/leads/<int:pk>/edit/', views.employer_lead_update, name='employer_lead_update'),
    path('admin/leads/<int:pk>/delete/', views.employer_lead_delete, name='employer_lead_delete'),
    
    # Blog CRUD
    path('admin/blogs/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('admin/blogs/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('admin/blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    
    # Case Study CRUD
    path('admin/case-studies/create/', views.CaseStudyCreateView.as_view(), name='case_study_create'),
    path('admin/case-studies/<int:pk>/edit/', views.CaseStudyUpdateView.as_view(), name='case_study_update'),
    path('admin/case-studies/<int:pk>/delete/', views.CaseStudyDeleteView.as_view(), name='case_study_delete'),
    
    # Resource CRUD
    path('admin/resources/create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('admin/resources/<int:pk>/edit/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('admin/resources/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),
    
    # Contact Messages CRUD
    path('admin/messages/', views.contact_message_list, name='contact_message_list'),
    path('admin/messages/<int:pk>/', views.contact_message_detail, name='contact_message_detail'),
    path('admin/messages/<int:pk>/delete/', views.contact_message_delete, name='contact_message_delete'),
    
    # Dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

