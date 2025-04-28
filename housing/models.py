from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('owner', 'Owner'), ('admin', 'Admin')], default='student')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  

    def __str__(self):
        return self.email
    

    def get_role_display(self):
        """Human-readable role name"""
        return dict(self._meta.get_field('role').choices).get(self.role, self.role)



class House(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'owner'})
    title = models.CharField(max_length=100)
    address = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    # Add other house fields as needed

    def __str__(self):
        return self.title
    


class RentalAgreement(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.student} renting {self.house}"
    

User = get_user_model()

class Rental(models.Model):
    house = models.ForeignKey('House', on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')

    def __str__(self):
        return f"{self.student.username} - {self.house.title}"