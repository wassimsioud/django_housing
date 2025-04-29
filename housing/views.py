from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm, HouseForm, ProfileForm, RentalForm
from django.contrib.auth.decorators import login_required
from .permissions import owner_required, student_required
from .models import House, RentalAgreement, Rental
from django.contrib import messages


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username') 
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
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile') 
    else:
        form = ProfileForm(instance=request.user)
    
    return render(request, 'profile/profile.html', {'form': form})





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




@login_required
@student_required
def student_dashboard(request):
    """View for student's rental dashboard"""
    rentals = Rental.objects.filter(student=request.user)
    return render(request, 'students/dashboard.html', {'rentals': rentals})


@login_required
def rent_house(request, house_id):
    house = get_object_or_404(House, id=house_id, is_available=True)
    
    if request.user.role != 'student':
        messages.error(request, "Only students can rent houses")
        return redirect('listings')
    
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.house = house
            rental.student = request.user
            rental.save()
            
            house.is_available = False
            house.save()
            
            messages.success(request, "House rented successfully!")
            return redirect('student_dashboard')
    else:
        form = RentalForm()
    
    return render(request, 'houses/rent.html', {
        'house': house,
        'form': form
    })