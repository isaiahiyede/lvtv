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
from general.models import UserAccount
from client.models import ProvideHelp, GetHelp
from datetime import timedelta  


# Create your models here.


class MatchParticipants(models.Model):
	user                     = models.ForeignKey(User,null=True, blank=True)
	receiver                 = models.ForeignKey(User,null=True, blank=True, related_name="Receiver")
	giver                    = models.ForeignKey(User,null=True, blank=True, related_name="Giver")
	providehelp 			 = models.ForeignKey(ProvideHelp,null=True, blank=True)
	gethelp 				 = models.ForeignKey(GetHelp, null=True, blank=True)
	amount_paired            = models.CharField(max_length=150, null=True, blank=True)
	confirmation_image       = models.ImageField(upload_to="confirmation", null=True, blank=True)
	paired                   = models.BooleanField(default=False)
	confirmed                = models.BooleanField(default=False)
	payment_made             = models.BooleanField(default=False)
	payment_received         = models.BooleanField(default=False)
	amt_matched              = models.FloatField(max_length=50, default=0)
	deleted 				 = models.BooleanField(default=False)
	track_order              = models.CharField(max_length=30, null=True, blank=True)
	created_on               = models.DateTimeField(auto_now_add = True)
	 

	def __unicode__(self):
		return unicode(self.user)
	
	class Meta:
		ordering = ['-created_on']
		verbose_name_plural = "Matched Participants"
	
	def get_all_messages(self):
		return self.messagecentercomment_set.all()
	
	def get_all_messages_count(self):
		return self.get_all_messages().count()
	
	def time_left_after_5_days(self):
		return self.created_on + timedelta(seconds = 432000)



class MessageCenterComment(models.Model):
	user                = models.ForeignKey(User, null=True)
	created_on          = models.DateTimeField(default = timezone.now)
	message             = models.TextField()
	no_of_comments      = models.IntegerField(default=0)
	new                 = models.BooleanField(default = True)
	replied             = models.BooleanField(default=False)
	resolved            = models.BooleanField(default=False)
	replied_on          = models.DateTimeField(null = True)
	archive             = models.BooleanField(default=False)
	providehelp         = models.ForeignKey(ProvideHelp, null=True, blank=True)
	gethelp             = models.ForeignKey(GetHelp, null=True, blank=True)
	matches             = models.OneToOneField(MatchParticipants, null=True, blank=True)
	date                = models.DateTimeField(default = timezone.now)
	admin               = models.BooleanField(default=False)
	subject             = models.CharField(max_length=150, null=True, blank=True)
	image_obj           = models.ImageField(upload_to="image_obj", null=True, blank=True)
	deleted				= models.BooleanField(default=False)
	
	
	def __unicode__(self):
		return unicode(self.date)
	
	def get_comments(self):
		return self.comment_set.all()

	def get_commnets_count(self):
		comments_count = self.get_comments().count()
		return comments_count
	
	class Meta:
		verbose_name_plural = 'Messages'
		

class Comment(models.Model):
	user                    = models.ForeignKey(User, null=True)
	message                 = models.TextField()
	date                    = models.DateTimeField(default = timezone.now)
	message_obj             = models.ForeignKey(MessageCenterComment, null=True, blank=True)
	support_admin           = models.BooleanField(default=False)
	image_obj               = models.ImageField(upload_to="image_obj", null=True, blank=True)

	
	def __unicode__(self):
		return unicode(self.user)
	
	class Meta:
			verbose_name_plural = 'Comments'



