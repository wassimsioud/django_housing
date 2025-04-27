from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, HouseForm
from django.contrib.auth.decorators import login_required
from .permissions import owner_required, student_required
from .models import House, RentalAgreement

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # redirect to home page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # AuthenticationForm uses 'username' field internally
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')





@login_required
@owner_required
def create_house(request):
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            house = form.save(commit=False)
            house.owner = request.user
            house.save()
            return redirect('owner_dashboard')
    else:
        form = HouseForm()
    return render(request, 'houses/create.html', {'form': form})



def listings_view(request):
    """Show all available houses for rent"""
    houses = House.objects.filter(is_available=True)
    return render(request, 'listings/listings.html', {'houses': houses})



@login_required
@student_required
def view_houses(request):
    houses = House.objects.filter(is_available=True)
    return render(request, 'houses/list.html', {'houses': houses})

@login_required
@student_required
def rent_house(request, house_id):
    house = get_object_or_404(House, pk=house_id, is_available=True)
    if request.method == 'POST':
        RentalAgreement.objects.create(
            house=house,
            student=request.user,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date')
        )
        house.is_available = False
        house.save()
        return redirect('student_dashboard')
    return render(request, 'houses/rent.html', {'house': house})


@login_required
@owner_required
def owner_dashboard(request):
    """Dashboard view for property owners"""
    houses = House.objects.filter(owner=request.user)
    return render(request, 'owners/dashboard.html', {'houses': houses})