from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import MaintenanceRequestForm, EmailUpdateForm
from .models import Property, Tenant, Lease, MaintenanceRequest, Profile
# from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required


def property_list(request):
    properties = Property.objects.all()
    search_query = request.GET.get('q', '')
    property_type = request.GET.get('property_type', '')
    min_rent = request.GET.get('min_rent', '')
    max_rent = request.GET.get('max_rent', '')
    properties = Property.objects.all()

    if search_query:
        properties = properties.filter(name__icontains=search_query)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if min_rent:
        properties = properties.filter(rent__gte=min_rent)
    if max_rent:
        properties = properties.filter(rent__lte=max_rent)

    return render(request, 'property_list.html', {'properties': properties})

def property_detail(request, id):
    property = Property.objects.get(id=id)
    return render(request, 'property_detail.html', {'property': property})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('property-list')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')


# Admin Dashboard View
@staff_member_required
@login_required
def admin_dashboard(request):
    # Example data for the dashboard
    properties = Property.objects.all()
    tenants = Tenant.objects.all()
    leases = Lease.objects.all()

    # Assuming some statistics for occupancy rate and revenue
    occupancy_rate = (len(leases) / len(properties)) * 100 if properties else 0
    total_revenue = sum([lease.rent for lease in leases])

    context = {
        'properties': properties,
        'tenants': tenants,
        'leases': leases,
        'occupancy_rate': occupancy_rate,
        'total_revenue': total_revenue
    }

    return render(request, 'admin_dashboard.html', context)

# Landlord Dashboard View
@login_required
def landlord_dashboard(request):
    # Get properties associated with the current logged-in landlord
    landlord = request.user  # assuming user is linked to the landlord model
    properties = Property.objects.filter(owner=landlord)
    leases = Lease.objects.filter(property__in=properties)

    context = {
        'properties': properties,
        'leases': leases
    }

    return render(request, 'landlord_dashboard.html', context)

# Tenant Dashboard View
@login_required
def tenant_dashboard(request):
    tenant = Tenant.objects.get(user=request.user)
    # tenant = request.user
    leases = Lease.objects.filter(tenant=tenant)
    maintenance_requests = MaintenanceRequest.objects.filter(tenant=tenant)

    context = {
        'leases': leases,
        'maintenance_requests': maintenance_requests
    }

    return render(request, 'tenant_dashboard.html', {'tenant': tenant})

@login_required
def submit_maintenance_request(request):
    tenant = request.user.tenant  # Assuming tenant is linked to the user
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            maintenance_request = form.save(commit=False)
            maintenance_request.tenant = tenant
            maintenance_request.save()
            return redirect('tenant_dashboard')  # Redirect back to tenant dashboard or a success page
    else:
        form = MaintenanceRequestForm()

    return render(request, 'submit_maintenance_request.html', {'form': form})

@login_required
def landlord_maintenance_requests(request):
    # Get all maintenance requests for properties owned by the landlord
    landlord = request.user  # Assuming user is linked to landlord model
    properties = landlord.property_set.all()
    maintenance_requests = MaintenanceRequest.objects.filter(tenant__property__in=properties)

    context = {
        'maintenance_requests': maintenance_requests
    }

    return render(request, 'landlord_maintenance_requests.html', context)

def home(request):
    properties = Property.objects.all()  # Fetch properties to display
    return render(request, 'home.html', {'properties': properties})

@login_required
def profile(request):
    if request.method == 'POST':
        form = EmailUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your email has been updated!')
            return redirect('profile')
    else:
        form = EmailUpdateForm(instance=request.user)

    return render(request, 'profile.html', {'form': form})

# Redirection to user-specific dashboard after login
@login_required
def user_dashboard(request):
    # Get the current user's profile and role
    profile = request.user.profile
    role = profile.role  # Assuming 'role' is the field storing the user's role

    # Redirect to the appropriate dashboard based on the role
    if role == 'tenant':
        return redirect('tenant-dashboard')  # Redirect to tenant dashboard
    elif role == 'landlord':
        return redirect('landlord-dashboard')  # Redirect to landlord dashboard
    elif role == 'admin':
        return redirect('admin-dashboard')  # Redirect to admin dashboard
    else:
        return render(request, 'userhome.html', {'role': role})


def user_registration_view(request):
    # User registration logic
    user = User.objects.create_user(username="username", password="password")
    profile = Profile.objects.create(user=user, role='tenant')  # or any role


# Example function for a payment page
def payment_page(request, property_id):
    # Sample property data (replace with database query in production)
    property_data = {
        "id": property_id,
        "name": "Luxury Apartment",
        "price": 1200,  # Rent amount
        "currency": "USD",
    }

    if request.method == "POST":
        # Process payment here using Stripe, PayPal, or another gateway
        payment_method = request.POST.get("payment_method")
        if payment_method == "Stripe":
            # Redirect to a Stripe payment processor (example placeholder)
            return redirect(f"https://checkout.stripe.com/pay/{property_id}")
        elif payment_method == "PayPal":
            # Redirect to PayPal processor (example placeholder)
            return redirect(f"https://www.paypal.com/checkoutnow?token={property_id}")
        else:
            return HttpResponse("Unsupported payment method", status=400)

    # Render the payment page with property details
    return render(request, "payment_page.html", {"property": property_data})