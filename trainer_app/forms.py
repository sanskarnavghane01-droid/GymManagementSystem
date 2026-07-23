from django import forms
from .models import Trainer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TrainerRegistrationForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    specialization = forms.CharField(max_length=100, required=False)
    experience = forms.IntegerField(required=False)
    joining_date = forms.DateField(required=False)

    # Trainer ID is generated automatically in the view; no username field to validate here.

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords do not match.')
        return cleaned

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # add bootstrap class to every input widget for visibility
            existing = field.widget.attrs.get('class', '')
            classes = (existing + ' form-control').strip()
            field.widget.attrs['class'] = classes
        # Add helpful placeholder examples for clarity
        placeholders = {
            'full_name': 'e.g. John Doe',
            'email': 'you@example.com',
            'phone': 'e.g. 9876543210',
            'specialization': 'e.g. Strength Training',
            'experience': 'e.g. 3',
            'joining_date': 'YYYY-MM-DD',
            'password1': 'Choose a password',
            'password2': 'Repeat the password',
        }
        for key, text in placeholders.items():
            if key in self.fields:
                self.fields[key].widget.attrs['placeholder'] = text


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
