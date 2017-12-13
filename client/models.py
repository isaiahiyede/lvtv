from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
from django.utils import timezone
from django.conf import settings
import datetime
import markdown
from django.utils import timezone
from django.template.defaultfilters import slugify
from general.modelchoices import PACKAGES
from datetime import datetime  
from datetime import timedelta  


# Create your models here.

class Contributions(models.Model):
    user_account             = models.ForeignKey(User, null=True, blank=True)
    package         		 = models.CharField(max_length=250, null=True, blank=True, choices=PACKAGES)
    created_on               = models.DateTimeField(auto_now_add = True)
    edited_on            	 = models.DateTimeField(auto_now_add = True)
    deleted_on               = models.DateTimeField(auto_now_add = True)   
    completed         		 = models.BooleanField(default = False)
    message_text             = models.CharField(max_length=350, null=True, blank=True)
    amount         		     = models.CharField(max_length=150, null=True, blank=True)
    tracking_number          = models.CharField(max_length=30, null=True, blank=True)
    tAndC                    = models.BooleanField(default = False)
    status                   = models.CharField(max_length=50, default="New")
    help_requested           = models.BooleanField(default = False)
    help_provided            = models.BooleanField(default = False)
    rel_to                   = models.CharField(max_length=50, null=True, blank=True)
    amount_requested         = models.CharField(max_length=150, null=True, blank=True)
    paired                   = models.BooleanField(default = False)
    amt_paired               = models.FloatField(max_length=50, default=0)
    amt_left                 = models.FloatField(max_length=50, default=0)
    paired_rel_to            = models.BooleanField(default = False)
    testimony                = models.BooleanField(default = False)
    deleted                  = models.BooleanField(default = False)
    payment_made             = models.BooleanField(default = False)
    payment_received         = models.BooleanField(default = False)


    class Meta:
        ordering = ['-created_on']
        abstract = True
    
    def __unicode__(self):
        return '%s' %(self.tracking_number)

    def get_full_name(self):
        return '%s %s' %(self.user_account.first_name, self.user_account.last_name)

    def after_fifteen_days(self):
        amount = float(self.amount)
        return str((amount * 0.15) + (amount))

    def after_thirty_days(self):
        amount = float(self.amount)
        return str((amount * 0.30) + (amount))

    def type(self):
        if self.tracking_number[0:2] == 'PH':
            return 'Provide Help'
        else:
            return 'Get Help'

    def collection_date_after_15days(self):
        return self.created_on + timedelta(seconds = 1296000)

    def collection_date_after_30days(self):
        return self.created_on + timedelta(seconds = 2592000)

    def get_matched_orders(self):
        return self.matchparticipants_set.all()
        


class ProvideHelp(Contributions):
    provideHelp = models.BooleanField(default = False)
    
    class Meta:
        verbose_name_plural = "Provide Help"

    def getPHTotal(self):
        return self.aggregate(Sum('amount'))



class GetHelp(Contributions):
    getHelp = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "Get Help"

    def getGHTotal(self):
        return self.aggregate(Sum('amount'))



class Testimonials(models.Model):
    user                = models.ForeignKey(User, null=True, blank=True)
    testimony_ph        = models.ForeignKey(ProvideHelp, null=True, blank=True)
    testimony_gh        = models.ForeignKey(GetHelp, null=True, blank=True)
    message             = models.CharField(max_length=500, null=True, blank=True)
    testimony_image     = models.FileField(upload_to="confirmation", null=True, blank=True)
    created_on          = models.DateTimeField(auto_now_add = True)
    default_text        = models.CharField(max_length=350, null=True, blank=True)


    def __unicode__(self):
        return '%s' %(self.user.username)

    class Meta:
        verbose_name_plural = "Testimonials"







