from django import forms
from .models import WorkflowType

class WorkflowTypeForm(forms.ModelForm):
    class Meta:
        model = WorkflowType
        fields = ['workflow_name', 'workflow_code']
