from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
import datetime
import markdown
from django.utils import timezone
from django.template.defaultfilters import slugify
from modelchoices import TITLE, STATES, COUNTRY
from client.models import ProvideHelp, GetHelp



# Create your models here.


class UserAccount(models.Model):
    # all user fields
    user                     =    models.OneToOneField(User, null=True, blank=True)
    password2                =    models.CharField(max_length=50, blank=True, null=True)
    phone_number             =    models.CharField(max_length = 15, null = True, blank = True)
    title                    =    models.CharField(max_length=50, null=True, blank=True)
    address1         		 =    models.CharField(max_length=250, null=True, blank=True)
    address2         		 =    models.CharField(max_length=250, null=True, blank=True)
    city         		 	 =    models.CharField(max_length=250, null=True, blank=True)
    state         		 	 =    models.CharField(max_length=250, null=True, blank=True)
    country         		 =    models.CharField(max_length=250, null=True, blank=True)
    created_on               =    models.DateTimeField(null=True,blank=True)
    edited_on            	 =    models.DateTimeField(null=True,blank=True)
    deleted_on               =    models.DateTimeField(null=True,blank=True)
    updated_on               =    models.DateTimeField(null=True,blank=True)      
    completed         		 =    models.BooleanField(default = False)
    profile_up_to_date       =    models.BooleanField(default = False)
    bank_acc_number          =    models.CharField(max_length=150, null=True, blank=True)
    bank_name         		 =    models.CharField(max_length=150, null=True, blank=True)
    block                    =    models.BooleanField(default = False)
    referral                 =    models.CharField(max_length=150, null=True, blank=True)
    defaulter_msg            =    models.CharField(max_length=1000, null=True, blank=True)
    defaulter                =    models.BooleanField(default = False)

    
    def __unicode__(self):
        return '%s %s' %(self.user.first_name.upper(), self.user.last_name.upper())

    def get_all_help_provided(self):
        return self.providehelp_set.all()

    def get_all_help_received(self):
        return self.gethelp_set.all()

    def full_name(self):
        return '%s %s' %(self.user.first_name, self.user.last_name)

    def full_address(self):
        return '%s, %s, %s, %s, %s' %(self.addres1, self.address2, self.city, self.state, self.country)

    def get_refs(self):
        return self.referrals_set.all()


class Referrals(models.Model):
    user                     = models.ForeignKey(UserAccount, null=True, blank=True)
    email                    = models.CharField(max_length=50, null=True, blank=True)
    created_on               = models.DateTimeField(auto_now_add = True)


    def __unicode__(self):
        return '%s' %(self.email)


    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Referrals"












