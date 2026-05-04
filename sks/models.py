from django.db import models
from django.utils.text import slugify

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Job(TimeStampedModel):
    JOB_TYPE_CHOICES = (
        ('contract', 'Contract'),
        ('full_time', 'Full Time'),
        ('contract_to_hire', 'Contract to Hire'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    location = models.CharField(max_length=150)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    experience = models.CharField(max_length=100)
    skills = models.TextField()
    description = models.TextField()
    responsibilities = models.TextField(blank=True, null=True)
    salary = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.location}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Applicant(TimeStampedModel):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="applicants",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    skills = models.TextField(blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)

    STATUS_CHOICES = (
        ('new', 'New'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return f"{self.name} - {self.email}"


class EmployerLead(TimeStampedModel):
    company_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    requirement = models.TextField()
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    hiring_type = models.CharField(max_length=100, blank=True, null=True)

    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    def __str__(self):
        return self.company_name

class Blog(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    content = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=150, default="Admin")

    featured_image = models.ImageField(upload_to='blogs/', blank=True, null=True)

    # SEO Fields
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.CharField(max_length=255, blank=True, null=True)

    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class CaseStudy(TimeStampedModel):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    client_name = models.CharField(max_length=255, blank=True, null=True)

    problem = models.TextField()
    solution = models.TextField()
    result = models.TextField()
    metrics = models.CharField(max_length=255, blank=True, null=True)

    featured_image = models.ImageField(upload_to='case_studies/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Resource(TimeStampedModel):
    RESOURCE_TYPE = (
        ('guide', 'Guide'),
        ('ebook', 'Ebook'),
        ('template', 'Template'),
        ('article', 'Article'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()
    resource_type = models.CharField(max_length=50, choices=RESOURCE_TYPE)

    file = models.FileField(upload_to='resources/', blank=True, null=True)
    external_link = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContactMessage(TimeStampedModel):

    # BASIC INFO
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)

    # SUBJECT TYPE
    SUBJECT_CHOICES = (
        ('hiring', 'Hiring Inquiry'),
        ('job', 'Job Inquiry'),
        ('partnership', 'Partnership'),
        ('general', 'General Inquiry'),
    )
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='general')

    message = models.TextField()

    # REQUIREMENT DETAILS
    requirement_type = models.CharField(max_length=100, blank=True, null=True)
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    hiring_duration = models.CharField(max_length=100, blank=True, null=True)
    budget = models.CharField(max_length=100, blank=True, null=True)

    # MULTI-SERVICE SELECTION (CHECKBOX STYLE)
    SERVICES_CHOICES = (
        ('temporary', 'Temporary Staffing'),
        ('contract_to_hire', 'Contract-to-Hire'),
        ('direct_hire', 'Direct Hire'),
        ('payrolling', 'Payrolling'),
        ('dedicated_team', 'Dedicated Teams'),
    )
    services_interested = models.JSONField(blank=True, null=True)

    # SOURCE TRACKING
    SOURCE_CHOICES = (
        ('website', 'Website'),
        ('linkedin', 'LinkedIn'),
        ('referral', 'Referral'),
        ('google', 'Google Search'),
        ('other', 'Other'),
    )
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='website')

    # STATUS TRACKING
    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('proposal_sent', 'Proposal Sent'),
        ('converted', 'Converted'),
        ('closed', 'Closed'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    # ADMIN NOTES
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.email}"