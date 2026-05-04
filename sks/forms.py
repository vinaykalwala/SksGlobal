from django import forms
from .models import (
    Job, Applicant, EmployerLead, Blog, 
    CaseStudy, Resource, ContactMessage
)

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'location', 'job_type', 'experience',
            'skills', 'description', 'responsibilities', 
            'salary', 'is_active'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'responsibilities': forms.Textarea(attrs={'rows': 5}),
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

class ApplicantForm(forms.ModelForm):
    class Meta:
        model = Applicant
        fields = [
            'job', 'name', 'email', 'phone', 
            'resume', 'skills', 'experience', 'status'
        ]
        widgets = {
            'skills': forms.Textarea(attrs={'rows': 3}),
        }

class EmployerLeadForm(forms.ModelForm):
    class Meta:
        model = EmployerLead
        fields = [
            'company_name', 'contact_person', 'email', 'phone',
            'requirement', 'tech_stack', 'hiring_type', 'status'
        ]
        widgets = {
            'requirement': forms.Textarea(attrs={'rows': 4}),
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title', 'content', 'excerpt', 'author',
            'featured_image', 'meta_title', 'meta_description',
            'keywords', 'is_published'
        ]
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'excerpt': forms.Textarea(attrs={'rows': 3}),
        }

class CaseStudyForm(forms.ModelForm):
    class Meta:
        model = CaseStudy
        fields = [
            'title', 'client_name', 'problem', 'solution',
            'result', 'metrics', 'featured_image'
        ]
        widgets = {
            'problem': forms.Textarea(attrs={'rows': 5}),
            'solution': forms.Textarea(attrs={'rows': 5}),
            'result': forms.Textarea(attrs={'rows': 5}),
        }

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'title', 'description', 'resource_type',
            'file', 'external_link'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ContactMessageForm(forms.ModelForm):
    services_interested = forms.MultipleChoiceField(
        choices=ContactMessage.SERVICES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = ContactMessage
        fields = [
            'name', 'email', 'phone', 'company_name', 'subject',
            'message', 'requirement_type', 'tech_stack',
            'hiring_duration', 'budget', 'services_interested',
            'source'
        ]
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }