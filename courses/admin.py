from django.contrib import admin
from django.contrib import messages
from django.urls import path
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from .models import Course, Module, Task
from io import TextIOWrapper
import csv
from django.urls import reverse
from django.utils.html import format_html
from django.shortcuts import render
import logging
from django.utils.translation import gettext_lazy as _




class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    fields = ('name', 'theory_hours', 'practical_hours', 'fee')


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0
    fields = ('name', 'theory_hours', 'practical_hours', 'fee')


@admin.action(description="Generate Modules and Tasks Automatically")
def generate_modules_and_tasks(modeladmin, request, queryset):
    """
    Generate modules and tasks automatically for the selected courses.
    Ensures generated data matches the conditions of theory/practical hours and fees.
    """
    try:
        num_modules = 3  # Number of modules to generate
        tasks_per_module = 5  # Tasks per module

        for course in queryset:
            # Calculate module values
            module_fee = course.fee / num_modules
            module_theory_hours = course.theory_hours // num_modules
            module_practical_hours = course.practical_hours // num_modules

            modules_to_create = []

            for i in range(num_modules):
                module = Module(
                    course=course,
                    name=f"Module {i + 1}",
                    theory_hours=module_theory_hours,
                    practical_hours=module_practical_hours,
                    fee=module_fee
                )
                modules_to_create.append(module)


        messages.success(request, "Modules and tasks generated successfully.")
    except Exception as e:
        messages.error(request, f"Error generating modules and tasks: {str(e)}")



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'duration_months', 'theory_hours', 'practical_hours', 'fee','delete_button')
    #list_filter = ('duration_months',)
    search_fields = ('name', 'code')
    inlines = [ModuleInline]
    actions = [generate_modules_and_tasks]
    

    def delete_button(self, obj):
        """
        Add a delete button for each row in the list view.
        """
        url = reverse('admin:courses_course_delete', args=[obj.id])  # Adjust 'courses_course' to match your app and model name
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"  # Column header
    delete_button.allow_tags = True

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),
        ]
        return custom_urls + urls
    def changelist_view(self, request, extra_context=None):
        """
        Add an "Upload CSV" button above the admin list.
        """
        extra_context = extra_context or {}
        extra_context['upload_csv_url'] = reverse('admin:import_csv')
        return super().changelist_view(request, extra_context=extra_context)
    
   
    logging.basicConfig(level=logging.DEBUG)

    def import_csv(self, request):
        """
        Handle the CSV file upload and import the data.
        """
        if request.method == "POST":
            try:
                csv_file = request.FILES.get("csv_file")
                if not csv_file or not csv_file.name.endswith('.csv'):
                    messages.error(request, "Please upload a valid CSV file.")
                    return HttpResponseRedirect(request.path)

                data = csv.reader(TextIOWrapper(csv_file, encoding='utf-8'))
                next(data)  # Skip the header row

                for row in data:
                    if len(row) != 14:
                        logging.warning(f"Malformed row skipped: {row}")
                        continue

                    course_name, course_code, duration_months, theory_hours, practical_hours, fee, \
                        module_name, module_theory_hours, module_practical_hours, module_fee, \
                        task_name, task_theory_hours, task_practical_hours, task_fee = row

                    course, created = Course.objects.get_or_create(
                        name=course_name,
                        code=course_code,
                        defaults={
                            "duration_months": int(duration_months),
                            "theory_hours": int(theory_hours),
                            "practical_hours": int(practical_hours),
                            "fee": float(fee)
                        }
                    )

                    logging.debug(f"Course {'created' if created else 'retrieved'}: {course}")

                    module, created = Module.objects.get_or_create(
                        course=course,
                        name=module_name,
                        defaults={
                            "theory_hours": int(module_theory_hours),
                            "practical_hours": int(module_practical_hours),
                            "fee": float(module_fee)
                        }
                    )

                    logging.debug(f"Module {'created' if created else 'retrieved'}: {module}")

                    task = Task.objects.create(
                        module=module,
                        name=task_name,
                        theory_hours=int(task_theory_hours),
                        practical_hours=int(task_practical_hours),
                        fee=float(task_fee)
                    )

                    logging.debug(f"Task created: {task}")

                messages.success(request, "CSV imported successfully!")
                return HttpResponseRedirect(reverse('admin:courses_course_changelist'))
            except Exception as e:
                logging.error(f"Error processing CSV: {str(e)}")
                messages.error(request, f"Error processing CSV: {str(e)}")
                return HttpResponseRedirect(request.path)

        return render(request, 'admin/import_csv.html', {"title": "Import CSV"})
    
@admin.action(description="Generate Tasks Automatically")
def generate_tasks(modeladmin, request, queryset):
    """
    Generate tasks automatically for the selected modules based on their theory hours,
    practical hours, and fee distribution.
    """
    try:
        tasks_per_module = 5  # Number of tasks to generate per module

        for module in queryset:
            # Calculate values for each task
            task_theory_hours = module.theory_hours // tasks_per_module
            task_practical_hours = module.practical_hours // tasks_per_module
            task_fee = module.fee / tasks_per_module

            tasks_to_create = []

            for i in range(tasks_per_module):
                task_name = f"Task {i + 1} in {module.name}"
                tasks_to_create.append(
                    Task(
                        module=module,
                        name=task_name,
                        theory_hours=task_theory_hours,
                        practical_hours=task_practical_hours,
                        fee=task_fee
                    )
                )

            # Bulk create tasks
            Task.objects.bulk_create(tasks_to_create)

        messages.success(request, "Tasks generated successfully.")
    except Exception as e:
        messages.error(request, f"Error generating tasks: {str(e)}")


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'theory_hours', 'practical_hours', 'fee','delete_button')
    #list_filter = ('course',)
    search_fields = ('name', 'course__name')
    inlines = [TaskInline]
    actions = [generate_tasks]
    def delete_button(self, obj):
        url = reverse('admin:courses_module_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'theory_hours', 'practical_hours', 'fee','delete_button')
    list_filter = ('module',)
    search_fields = ('name', 'module__name')
    def delete_button(self, obj):
        url = reverse('admin:courses_task_delete', args=[obj.id])  # Adjust as necessary
        return format_html('<a class="button" href="{}">Delete</a>', url)

    delete_button.short_description = "Delete"
    delete_button.allow_tags = True


