from django import forms
from general.models import UserAccount
from django.forms import ModelForm, Textarea
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from client.models import *
from general.modelchoices import PACKAGES
#from captcha.fields import CaptchaField
# from nocaptcha_recaptcha.fields import NoReCaptchaField
# from general.modelfield_choices import HOW_DID_YOU_FIND_US, INDUSTRY, PAYMENT

attrs3 = {'class': 'form-control','required': 'true'}


class ProvideHelpForm(forms.ModelForm):
    amount          = forms.ChoiceField(choices=PACKAGES, widget=forms.Select(attrs=attrs3))
    tAndC           = forms.BooleanField(required=True)
     
    class Meta:
        model = ProvideHelp
        fields = ('amount', 'tAndC',)


class GetHelpForm(forms.ModelForm):
    amount          = forms.ChoiceField(choices=PACKAGES, widget=forms.Select(attrs=attrs3))
    tAndC           = forms.BooleanField(required=True)
     
    class Meta:
        model = GetHelp
        fields = ('amount', 'tAndC',)
