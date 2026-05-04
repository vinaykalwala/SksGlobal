from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from sks import views

urlpatterns = [

    # ------------------ CORE ------------------
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ------------------ STATIC PAGES ------------------
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact_view, name='contact'),  # ✅ fixed duplicate
    path('contact/success/', views.contact_success, name='contact_success'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_of_service, name='terms'),

    # ------------------ JOBS ------------------
    path('jobs/', views.JobListView.as_view(), name='job_list'),
    path('jobs/create/', views.JobCreateView.as_view(), name='job_create'),
    path('jobs/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('jobs/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('jobs/<slug:slug>/', views.JobDetailView.as_view(), name='job_detail'),
    path('jobs/<slug:slug>/apply/', views.apply_for_job, name='apply_for_job'),

    # ------------------ BLOGS ------------------
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
    path('blogs/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),

    # ------------------ CASE STUDIES ------------------
    path('case-studies/', views.CaseStudyListView.as_view(), name='case_study_list'),
    path('case-studies/create/', views.CaseStudyCreateView.as_view(), name='case_study_create'),
    path('case-studies/<int:pk>/edit/', views.CaseStudyUpdateView.as_view(), name='case_study_update'),
    path('case-studies/<int:pk>/delete/', views.CaseStudyDeleteView.as_view(), name='case_study_delete'),
    path('case-studies/<slug:slug>/', views.CaseStudyDetailView.as_view(), name='case_study_detail'),

    # ------------------ RESOURCES ------------------
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/create/', views.ResourceCreateView.as_view(), name='resource_create'),
    path('resources/<int:pk>/edit/', views.ResourceUpdateView.as_view(), name='resource_update'),
    path('resources/<int:pk>/delete/', views.ResourceDeleteView.as_view(), name='resource_delete'),
    path('resources/<slug:slug>/', views.ResourceDetailView.as_view(), name='resource_detail'),

    # ------------------ APPLICANTS ------------------
    path('applicants/', views.applicant_list, name='applicant_list'),
    path('applicants/<int:pk>/', views.applicant_detail, name='applicant_detail'),
    path('applicants/<int:pk>/edit/', views.applicant_update, name='applicant_update'),
    path('applicants/<int:pk>/delete/', views.applicant_delete, name='applicant_delete'),

    # ------------------ LEADS ------------------
    path('leads/', views.employer_lead_list, name='employer_lead_list'),
    path('leads/create/', views.employer_lead_create, name='employer_lead_create'),
    path('leads/<int:pk>/', views.employer_lead_detail, name='employer_lead_detail'),
    path('leads/<int:pk>/edit/', views.employer_lead_update, name='employer_lead_update'),
    path('leads/<int:pk>/delete/', views.employer_lead_delete, name='employer_lead_delete'),

    # ------------------ CONTACT MESSAGES ------------------
    path('messages/', views.contact_message_list, name='contact_message_list'),
    path('messages/<int:pk>/', views.contact_message_detail, name='contact_message_detail'),
    path('messages/<int:pk>/delete/', views.contact_message_delete, name='contact_message_delete'),

    # ------------------ DASHBOARD ------------------
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

# ------------------ STATIC / MEDIA ------------------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)