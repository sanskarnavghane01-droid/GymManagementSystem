from django import forms
from .models import Trainer


class TrainerForm(forms.ModelForm):
    is_trainer = forms.BooleanField(required=False, label='Trainer')

    class Meta:
        model = Trainer
        fields = [
            'full_name',
            'email',
            'phone',
            'gender',
            'specialization',
            'experience',
            'joining_date',
            'status',
            'address',
        ]
