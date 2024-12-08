from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import Group, User
from django.views.generic import TemplateView, ListView
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import logging
import joblib  # Assuming you're using a pre-trained model saved with joblib
import pandas as pd
import os
from django.conf import settings
from django.core.mail import send_mail

from predictions.models import Activity, MarksTracker

# Initialize logger
logger = logging.getLogger(__name__)

# Define normalize_input function
def normalize_input(input_data):
    """Normalize input data using the fitted scaler."""
    scaler_path = os.path.join(settings.BASE_DIR, 'users/models/scaler_vdataset.pkl')
    scaler = joblib.load(scaler_path)

    # Make sure these match the features used during model training
    columns = ['gender', 'num_of_prev_attempts', 'final_assessment_score', 
               'tasks_completed', 'practical_hours', 'theory_hours', 
               'exercises_completed', 'industry_training_experience']
    input_df = pd.DataFrame(input_data, columns=columns)
    return scaler.transform(input_df)

def predict_grade(request, student_id):
    """Handles student final grade prediction."""
    if request.method == 'POST':
        try:
            # Retrieve the student's MarksTracker based on student_id
            marks_tracker = get_object_or_404(MarksTracker, student_id=student_id)
            logger.debug("Starting grade prediction process for student_id: %s", student_id)

            # Load your pre-trained model using the correct path
            model_path = os.path.join(settings.BASE_DIR, 'users/models/fine_tuned_model.pkl')
            model = joblib.load(model_path)

            # Convert gender to binary
            gender_binary = 1 if marks_tracker.student.profile.gender == 'F' else 0

            # Prepare the data for the model using the student's data
            input_data = [[
                gender_binary,
                marks_tracker.num_of_prev_attempts,
                marks_tracker.final_assessment_score,
                marks_tracker.tasks_completed,
                marks_tracker.practical_hours,
                marks_tracker.theory_hours,
                marks_tracker.exercises_completed,
                marks_tracker.industry_training_experience
            ]]

            # Normalize the input data
            normalized_data = normalize_input(input_data)

            # Predict the final grade using the trained model
            predicted_grade = model.predict(normalized_data)[0]
            #predicted_grade="pass"
            # Update the student's final grade in MarksTracker
            marks_tracker.final_grade = predicted_grade
            marks_tracker.save()
            if predicted_grade==1:
                grade="Pass"
            else:
                grade ="Fail"
            logger.debug("Prediction completed successfully: Final Grade %s", predicted_grade)
            print(predicted_grade)

            # Send real-time notification to the teacher (optional)
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": f"New final grade predicted for student {marks_tracker.student.first_name}: {predicted_grade}"
                }
            )
    
            student_email = marks_tracker.student.email
            send_mail(
                subject='Your Final Grade Prediction',
                message=f'Dear {marks_tracker.student.first_name},\n\n'
                        f'Your final grade has been predicted as: {grade}. '
                        f'Please check the dashboard for more details.\n\n'
                        'Best regards,\nYour School Team',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student_email],
                fail_silently=False,
            )
            logger.debug("Email sent successfully to student: %s", student_email)
            # Redirect back to the teacher's dashboard
            #return redirect('teacher_dashboard')
            return render(request, 'predictions/result.html', {'result': grade})

        except Exception as e:
            logger.error("Error during grade prediction: %s", e)
            return render(request, 'predictions/result.html', {'result': f'Error: {str(e)}'})

    # Handle GET request: Show the form
    return render(request, 'predictions/index.html')


# Custom Login View
class CustomLoginView(LoginView):
    template_name = 'users/login.html'  # Path to your custom login template

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse_lazy('admin:index')  # Redirect admin to admin site
        elif user.groups.filter(name='Student').exists():
            return reverse_lazy('student_dashboard')
        elif user.groups.filter(name='Teacher').exists():
            return reverse_lazy('teacher_dashboard')
        elif user.groups.filter(name='Staff').exists():
            return reverse_lazy('staff_dashboard')
        else:
            return reverse_lazy('default_dashboard')  # Redirect regular users to their home page


# Home View for Regular Users
class UserHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'user_home.html'  # Regular user home page
    login_url = 'login'  # Redirect if the user is not logged in


# Student Dashboard
class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_dashboard.html'
    login_url = 'login'  # Redirect to login if not authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activities = Activity.objects.filter(student=self.request.user)
        marks_tracker, created = MarksTracker.objects.get_or_create(student=self.request.user)

        context['activities'] = activities
        context['marks_tracker'] = marks_tracker
        return context


# Teacher Dashboard
class TeacherDashboardView(LoginRequiredMixin, ListView):
    template_name = 'teacher_dashboard.html'
    login_url = 'login'
    model = MarksTracker  # Fetching MarksTracker objects
    context_object_name = 'marks_trackers'  # The name of the context in the template
    #predict_grade(request, student_id)
    def get_queryset(self):
        return MarksTracker.objects.all()

    def post(self, request, *args, **kwargs):
        # Handle POST request for grade prediction
        student_id = kwargs.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        
        # Retrieve the student's marks and predict the grade
        marks_tracker = MarksTracker.objects.filter(student=student)
        predicted_grade = predict_grade(marks_tracker)
        
        # Process the predicted grade (e.g., show it in the dashboard or redirect)
        # Here, you could redirect or update the context to show the predicted grade
        return HttpResponseRedirect(reverse('teacher_dashboard'))  # Redirect back to the dashboard

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Additional context or predicted grades can be added here
        return context
   
# Staff Dashboard
class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'staff_dashboard.html'
    login_url = 'login'


# Profile View Example
class ProfileView(TemplateView):
    template_name = 'profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = 'Nina Mcintire'
        context['followers'] = 1322
        context['following'] = 543
        context['friends'] = 13287
        context['education'] = 'B.S. in Computer Science from the University of Tennessee at Knoxville'
        context['location'] = 'Malibu, California'
        context['skills'] = ['UI Design', 'Coding', 'Javascript', 'PHP', 'Node.js']
        context['notes'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        return context

