from django.contrib.auth import views as auth_views
from django.urls import path
from . import views  # Import the views module
from .views import ProfileView,predict_grade


app_name = 'users'  # Add the namespace here

urlpatterns = [
    
   
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout URL
path('profile/', ProfileView.as_view(), name='profile'),
  path('teacher/predict-grade/<int:student_id>/', predict_grade, name='predict_grade'),
    

]







