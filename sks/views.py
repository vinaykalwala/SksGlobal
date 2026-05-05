from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .models import (
    Job, Applicant, EmployerLead, Blog, 
    CaseStudy, Resource, ContactMessage
)
from .forms import (
    JobForm, ApplicantForm, EmployerLeadForm, BlogForm,
    CaseStudyForm, ResourceForm, ContactMessageForm
)

def home(request):
    jobs = Job.objects.filter(is_active=True)[:5]
    blogs = Blog.objects.filter(is_published=True)[:3]

    return render(request, 'home.html', {
        'jobs': jobs,
        'blogs': blogs
    })


def about(request):
    return render(request, 'about.html')


def services(request):
    return render(request, 'services.html')


def contact(request):
    return render(request, 'contact.html')


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


def terms_of_service(request):
    return render(request, 'terms.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')

def admin_required(view_func):
    decorated = login_required(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('home')
        return decorated(request, *args, **kwargs)
    return wrapper

# ============= JOB VIEWS =============
class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'jobs'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True)
        job_type = self.request.GET.get('type')
        location = self.request.GET.get('location')
        
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job_types'] = Job.JOB_TYPE_CHOICES
        return context

class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'
    context_object_name = 'job'

@method_decorator(admin_required, name='dispatch')
class JobCreateView(CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('job_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Job created successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('job_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Job updated successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class JobDeleteView(DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Job deleted successfully!")
        return super().delete(request, *args, **kwargs)

# ============= APPLICANT VIEWS =============
@admin_required
def applicant_list(request):
    applicants = Applicant.objects.select_related('job').all()
    status_filter = request.GET.get('status')
    job_filter = request.GET.get('job')
    
    if status_filter:
        applicants = applicants.filter(status=status_filter)
    if job_filter:
        applicants = applicants.filter(job_id=job_filter)
    
    paginator = Paginator(applicants, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'applicants': page_obj,
        'status_choices': Applicant.STATUS_CHOICES,
        'jobs': Job.objects.filter(is_active=True),
    }
    return render(request, 'applicant_list.html', context)

@admin_required
def applicant_detail(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    return render(request, 'applicant_detail.html', {'applicant': applicant})

@admin_required
def applicant_update(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES, instance=applicant)
        if form.is_valid():
            form.save()
            messages.success(request, "Applicant updated successfully!")
            return redirect('applicant_detail', pk=applicant.pk)
    else:
        form = ApplicantForm(instance=applicant)
    
    return render(request, 'applicant_form.html', {'form': form, 'applicant': applicant})

@admin_required
def applicant_delete(request, pk):
    applicant = get_object_or_404(Applicant, pk=pk)
    if request.method == 'POST':
        applicant.delete()
        messages.success(request, "Applicant deleted successfully!")
        return redirect('applicant_list')
    return render(request, 'applicant_confirm_delete.html', {'applicant': applicant})

# ============= EMPLOYER LEAD VIEWS =============
@admin_required
def employer_lead_list(request):
    leads = EmployerLead.objects.all()
    status_filter = request.GET.get('status')
    
    if status_filter:
        leads = leads.filter(status=status_filter)
    
    paginator = Paginator(leads, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'leads': page_obj,
        'status_choices': EmployerLead.STATUS_CHOICES,
    }
    return render(request, 'employer_lead_list.html', context)

@admin_required
def employer_lead_detail(request, pk):
    lead = get_object_or_404(EmployerLead, pk=pk)
    return render(request, 'employer_lead_detail.html', {'lead': lead})

def employer_lead_create(request):
    if request.method == 'POST':
        form = EmployerLeadForm(request.POST)
        if form.is_valid():
            form.save()  # <-- typo fixed (befoe removed)
            messages.success(request, "Employer lead created successfully!")
            return redirect('employer_lead_list')
    else:
        form = EmployerLeadForm()
    
    return render(request, 'employer_lead_form.html', {'form': form})

@admin_required
def employer_lead_update(request, pk):
    lead = get_object_or_404(EmployerLead, pk=pk)
    if request.method == 'POST':
        form = EmployerLeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            messages.success(request, "Lead updated successfully!")
            return redirect('employer_lead_detail', pk=lead.pk)
    else:
        form = EmployerLeadForm(instance=lead)
    
    return render(request, 'employer_lead_form.html', {'form': form, 'lead': lead})

@admin_required
def employer_lead_delete(request, pk):
    lead = get_object_or_404(EmployerLead, pk=pk)
    if request.method == 'POST':
        lead.delete()
        messages.success(request, "Lead deleted successfully!")
        return redirect('employer_lead_list')
    return render(request, 'employer_lead_confirm_delete.html', {'lead': lead})

# ============= BLOG VIEWS =============
class BlogListView(ListView):
    model = Blog
    template_name = 'blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 9
    
    def get_queryset(self):
        return Blog.objects.filter(is_published=True).order_by('-created_at')

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    context_object_name = 'blog'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count if you add a view_count field
        return obj

@method_decorator(admin_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Blog post created successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'blog_form.html'
    success_url = reverse_lazy('blog_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Blog post updated successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = 'blog_confirm_delete.html'
    success_url = reverse_lazy('blog_list')

# ============= CASE STUDY VIEWS =============
class CaseStudyListView(ListView):
    model = CaseStudy
    template_name = 'case_study_list.html'
    context_object_name = 'case_studies'
    paginate_by = 6

class CaseStudyDetailView(DetailView):
    model = CaseStudy
    template_name = 'case_study_detail.html'
    context_object_name = 'case_study'

@method_decorator(admin_required, name='dispatch')
class CaseStudyCreateView(CreateView):
    model = CaseStudy
    form_class = CaseStudyForm
    template_name = 'case_study_form.html'
    success_url = reverse_lazy('case_study_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Case study created successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class CaseStudyUpdateView(UpdateView):
    model = CaseStudy
    form_class = CaseStudyForm
    template_name = 'case_study_form.html'
    success_url = reverse_lazy('case_study_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Case study updated successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class CaseStudyDeleteView(DeleteView):
    model = CaseStudy
    template_name = 'case_study_confirm_delete.html'
    success_url = reverse_lazy('case_study_list')

# ============= RESOURCE VIEWS =============
class ResourceListView(ListView):
    model = Resource
    template_name = 'resource_list.html'
    context_object_name = 'resources'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Resource.objects.all()
        resource_type = self.request.GET.get('type')
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['resource_types'] = Resource.RESOURCE_TYPE
        return context

class ResourceDetailView(DetailView):
    model = Resource
    template_name = 'resource_detail.html'
    context_object_name = 'resource'

@method_decorator(admin_required, name='dispatch')
class ResourceCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resource_form.html'
    success_url = reverse_lazy('resource_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Resource created successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class ResourceUpdateView(UpdateView):
    model = Resource
    form_class = ResourceForm
    template_name = 'resource_form.html'
    success_url = reverse_lazy('resource_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Resource updated successfully!")
        return super().form_valid(form)

@method_decorator(admin_required, name='dispatch')
class ResourceDeleteView(DeleteView):
    model = Resource
    template_name = 'resource_confirm_delete.html'
    success_url = reverse_lazy('resource_list')

# ============= CONTACT MESSAGE VIEWS =============
def contact_view(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
            # You can add email notification here
            return redirect('contact_success')
    else:
        form = ContactMessageForm()
    
    return render(request, 'contact.html', {'form': form})

def contact_success(request):
    return render(request, 'contact_success.html')

@admin_required
def contact_message_list(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    status_filter = request.GET.get('status')
    subject_filter = request.GET.get('subject')
    
    if status_filter:
        messages_list = messages_list.filter(status=status_filter)
    if subject_filter:
        messages_list = messages_list.filter(subject=subject_filter)
    
    paginator = Paginator(messages_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'messages': page_obj,
        'status_choices': ContactMessage.STATUS_CHOICES,
        'subject_choices': ContactMessage.SUBJECT_CHOICES,
    }
    return render(request, 'contact_message_list.html', context)

@admin_required
def contact_message_detail(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        # Update status and admin notes
        message.status = request.POST.get('status')
        message.admin_notes = request.POST.get('admin_notes')
        message.save()
        messages.success(request, "Message updated successfully!")
        return redirect('contact_message_detail', pk=message.pk)
    
    return render(request, 'contact_message_detail.html', {'message': message})

@admin_required
def contact_message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, "Message deleted successfully!")
        return redirect('contact_message_list')
    return render(request, 'contact_message_confirm_delete.html', {'message': message})

# ============= DASHBOARD VIEW =============
@admin_required
def admin_dashboard(request):
    context = {
        'total_jobs': Job.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'total_applicants': Applicant.objects.count(),
        'new_applicants': Applicant.objects.filter(status='new').count(),
        'total_leads': EmployerLead.objects.count(),
        'new_leads': EmployerLead.objects.filter(status='new').count(),
        'total_messages': ContactMessage.objects.count(),
        'unread_messages': ContactMessage.objects.filter(status='new').count(),
        'total_blogs': Blog.objects.filter(is_published=True).count(),
        'total_case_studies': CaseStudy.objects.count(),
        'total_resources': Resource.objects.count(),
    }
    return render(request, 'admin_dashboard.html', context)

# ============= PUBLIC JOB APPLICATION VIEW =============
def apply_for_job(request, slug):
    job = get_object_or_404(Job, slug=slug, is_active=True)
    if request.method == 'POST':
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():
            applicant = form.save(commit=False)
            applicant.job = job
            applicant.save()
            messages.success(request, f"Your application for {job.title} has been submitted successfully!")
            return redirect('job_detail', slug=job.slug)
    else:
        form = ApplicantForm(initial={'job': job})
        # Hide job field from form
        form.fields['job'].widget = forms.HiddenInput()
    
    return render(request, 'apply_for_job.html', {'form': form, 'job': job})