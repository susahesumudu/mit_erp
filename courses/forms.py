from django import forms

class AutoGenerateForm(forms.Form):
    num_modules = forms.IntegerField(label="Number of Modules", min_value=1)
    tasks_per_module = forms.IntegerField(label="Tasks per Module", min_value=0)
