from django import forms
from django.contrib.auth.models import User
from .models import Feedback

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['order', 'question', 'answer']

