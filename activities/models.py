from django.db import models

# Create your models here.
class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('Exercise', 'Exercise'),
        ('Assignment', 'Assignment'),
        ('Project', 'Project'),
    ]

    SESSION_TYPES = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
    ]

   
    title = models.CharField(max_length=100)
    description = models.TextField()
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    grading_rubric = models.TextField()  # Rubric details
    publish_grading_rubric = models.BooleanField(default=False)  # Option to publish rubric
    submission_deadline = models.DateTimeField()  # Deadline for submission
    session_type = models.CharField(max_length=10, choices=SESSION_TYPES)
  

    def __str__(self):
        return self.title

class Submission(models.Model):
    activity = models.ForeignKey(Activity, related_name='submissions', on_delete=models.CASCADE)
    #student = models.ForeignKey(User, related_name='submissions', on_delete=models.CASCADE)  # Assuming User model
    submission_file = models.FileField(upload_to='submissions/')  # File upload
    submitted_at = models.DateTimeField(auto_now_add=True)  # Automatically set to now when submitted
    marks = models.FloatField(null=True, blank=True)  # Marks can be assigned later
    feedback = models.TextField(null=True, blank=True)  # Optional feedback for the submission
    submitted_at = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True) 


    def duration(self):
        return (self.end_time - self.start_time).total_seconds() / 3600  # Duration in hours

    def is_achieved_on_time(self):
        now = timezone.now()
        if now > self.submission_deadline:
            return 'Late'
        elif now < self.submission_deadline:
            return 'Earlier'
        return 'On Time'

    def is_late(self):
        return self.submitted_at > self.activity.submission_deadline

    def __str__(self):
        return f"Submission by {self.student.username} for {self.activity.title}"


# models.py

class GradingRubric(models.Model):
    activity = models.ForeignKey(Activity, related_name='rubrics', on_delete=models.CASCADE)
    criteria = models.CharField(max_length=255)  # The criteria being graded
    description = models.TextField()  # Description of the criteria
    max_points = models.FloatField()  # Maximum points for this criteria
    points_awarded = models.FloatField(null=True, blank=True)  # Points awarded for this criteria

    def __str__(self):
        return f"{self.criteria} ({self.max_points} points)"
