from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
from django.core.exceptions import ValidationError



class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    duration_months = models.PositiveIntegerField()
    theory_hours = models.PositiveIntegerField()
    practical_hours = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validates the totals of related modules only if the course has been saved
        and related modules exist.
        """
        # Skip validation if the course is not yet saved
        if not self.pk:
            return

        # Check if related modules exist
        related_modules = self.modules.all()
        if not related_modules.exists():
            return

        # Validate totals only when modules are present
        total_module_theory_hours = sum(module.theory_hours for module in related_modules)
        total_module_practical_hours = sum(module.practical_hours for module in related_modules)
        total_module_fees = sum(module.fee for module in related_modules)

        if total_module_theory_hours != self.theory_hours:
            raise ValidationError("The sum of module theory hours must match the course theory hours.")
        if total_module_practical_hours != self.practical_hours:
            raise ValidationError("The sum of module practical hours must match the course practical hours.")
        if total_module_fees != self.fee:
            raise ValidationError("The sum of module fees must match the course fee.")

    def save(self, *args, **kwargs):
        """
        Save the instance without triggering validation prematurely.
        """
        super().save(*args, **kwargs)  # Save the course first
        self.clean()  # Run validation after saving

    def __str__(self):
        return self.name





from django.db import models
from django.core.exceptions import ValidationError

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    theory_hours = models.PositiveIntegerField()
    practical_hours = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Validates that the sum of task attributes matches the module attributes.
        Skips validation if tasks are not yet saved.
        """
        if not self.pk:  # Skip validation if the module is not yet saved
            return

        # Fetch related tasks only if they exist
        related_tasks = self.tasks.all()
        if not related_tasks.exists():
            return

        # Calculate totals for related tasks
        total_task_theory_hours = sum(task.theory_hours for task in related_tasks)
        total_task_practical_hours = sum(task.practical_hours for task in related_tasks)
        total_task_fees = sum(task.fee for task in related_tasks)

        # Perform validation checks
        if total_task_theory_hours != self.theory_hours:
            raise ValidationError("The sum of task theory hours must match the module theory hours.")
        if total_task_practical_hours != self.practical_hours:
            raise ValidationError("The sum of task practical hours must match the module practical hours.")
        if total_task_fees != self.fee:
            raise ValidationError("The sum of task fees must match the module fee.")

    def save(self, *args, **kwargs):
        """
        Save method to ensure validation is done after saving the module.
        """
        super().save(*args, **kwargs)  # Save the module first
        self.clean()  # Run validation after saving

    def __str__(self):
        return self.name




class Task(models.Model):
    module = models.ForeignKey(Module, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    theory_hours = models.PositiveIntegerField()
    practical_hours = models.PositiveIntegerField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the instance is created
    updated_at = models.DateTimeField(auto_now=True)      # Automatically updated when the instance is saved

    def __str__(self):
        return self.name