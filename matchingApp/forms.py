from django import forms
from django.contrib.auth.models import User
from matchingApp.models import *



attrs3 = {'required': 'true'}


class DateInput(forms.DateInput):
    input_type = 'date'



class CommentForm(forms.ModelForm):
	message        = forms.CharField(max_length = 128, help_text = "", widget=forms.Textarea(attrs={'required':'true'}))
	image_obj      = forms.ImageField(required = False, help_text='Photo', widget=forms.widgets.ClearableFileInput())

	class Meta:
	    model = Comment
	    fields = ('message', 'image_obj',)