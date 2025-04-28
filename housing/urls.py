from django.urls import path
from . import views

urlpatterns = [
    
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),



    # Owner URLs
    path('owner/houses/create/', views.create_house, name='create_house'),
    
    # Student URLs
    path('houses/', views.view_houses, name='view_houses'),
    path('houses/<int:house_id>/rent/', views.rent_house, name='rent_house'),


    path('owner/dashboard/', views.owner_dashboard, name='owner_dashboard'),
    

    path('listings/', views.listings_view, name='listings'),


    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),

    path('houses/<int:house_id>/rent/', views.rent_house, name='rent_house'),

]
