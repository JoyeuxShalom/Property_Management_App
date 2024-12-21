from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField(default=1)
    additional_info = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    images = models.ManyToManyField('PropertyImage', related_name='properties')

    def __str__(self):
        return self.name
class PropertyImage(models.Model):
    image = models.ImageField(upload_to='property_images/')

class Unit(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    number = models.CharField(max_length=10)
    size = models.IntegerField(help_text="Size in square meters")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Unit {self.number} at {self.property.name}"

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='tenants')

    def __str__(self):
        return self.user.username

class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Lease for {self.tenant.user.username} in {self.unit.property.name}"

# MaintenanceRequest Model
class MaintenanceRequest(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    issue = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    status_choices = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved')
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def __str__(self):
        return f"Maintenance Request by {self.tenant.user.username} - {self.status}"


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='tenant')

    def __str__(self):
        return f' {self.user.username} Profile'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, role='tenant')  # Default to 'tenant' or modify as needed