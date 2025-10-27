from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organization(models.Model):
    user = models.ManyToManyField(User, related_name="organizations")
    name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    logo = models.ImageField(
        upload_to="media/organization_logos", blank=True, null=True
    )

    def __str__(self):
        return self.name


class Branch(models.Model):
    user = models.ManyToManyField(User, related_name="branches")
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="branches"
    )
    name = models.CharField(max_length=30)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Agency(models.Model):
    user = models.ManyToManyField(User, related_name="agencies")
    branch = models.ForeignKey(
        Branch, on_delete=models.CASCADE, related_name="agencies"
    )
    logo = models.ImageField(
        upload_to="media/agency_logos", blank=True, null=True )
    name = models.CharField(max_length=30)
    ageny_name = models.CharField(max_length=30, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    agreement_status = models.BooleanField(default=False)
    
    # New fields for API 8
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    credit_limit_days = models.IntegerField(null=True, blank=True)

    AGENCY_TYPE_CHOICES = [
        ("Area Agency", "Area Agency"),
        ("Full Agency", "Full Agency"),
    ]
    agency_type = models.CharField(max_length=50, choices=AGENCY_TYPE_CHOICES, null=True, blank=True)

    # Auto-generated short agency identifier (6 chars)
    agency_id = models.CharField(max_length=6, unique=True, null=True, blank=True)

    # User who manages this agency
    assign_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="managed_agencies")

    def save(self, *args, **kwargs):
        # auto-generate a unique 6-char agency_id if not provided
        if not self.agency_id:
            import random, string

            for _ in range(10):
                candidate = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
                if not Agency.objects.filter(agency_id=candidate).exists():
                    self.agency_id = candidate
                    break
        super().save(*args, **kwargs)


class AgencyFiles(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to="media/agency_files/")
    file_type = models.CharField(max_length=50, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)


class AgencyContact(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    remarks = models.CharField(max_length=50, null=True, blank=True)


class OrganizationLink(models.Model):
    """Organization linking between two companies.
    Created by Super Admin only.
    """

    STATUS_PENDING = "PENDING"
    STATUS_ACCEPTED = "ACCEPTED"
    STATUS_REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pending"),
        (STATUS_ACCEPTED, "Accepted"),
        (STATUS_REJECTED, "Rejected"),
    ]

    main_organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="main_links"
    )
    link_organization = models.ForeignKey(
        "Organization",
        on_delete=models.CASCADE,
        related_name="linked_with"
    )
    link_organization_request = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    main_organization_request = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING
    )
    request_status = models.BooleanField(default=False)  # false until both accept
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "organization_links"
        managed = True

    def save(self, *args, **kwargs):
        # ✅ Auto-set request_status = True when both accepted
        if (
            self.link_organization_request == self.STATUS_ACCEPTED
            and self.main_organization_request == self.STATUS_ACCEPTED
        ):
            self.request_status = True
        else:
            self.request_status = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.main_organization} ↔ {self.link_organization} ({self.request_status})"
