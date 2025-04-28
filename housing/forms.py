from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser, House, RentalAgreement, Rental
from django.utils import timezone


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role')  # You can add more fields if needed

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')



class HouseForm(forms.ModelForm):
    class Meta:
        model = House
        exclude = ['owner', 'is_available']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class RentalAgreementForm(forms.ModelForm):
    class Meta:
        model = RentalAgreement
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }


User = get_user_model()

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
        }



class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date()}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date")
        
        return cleaned_data
