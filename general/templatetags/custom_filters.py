from django import template
from django.template.defaultfilters import stringfilter
from datetime import date, timedelta
from general.models import UserAccount
from client.models import *
#from export.models import *
import datetime
import time
import pytz
from django.db.models import Q, Sum
from itertools import chain
from operator import attrgetter
from datetime import datetime  
from datetime import timedelta
from client.models import *
from matchingApp.models import *


register = template.Library()


@register.simple_tag
def get_time_left(val1,val2):
	answer = str(val1 - val2).split('.')[0]
	if val1 <= val2:
		return 'Time Elasped'
	else:
		return answer


@register.simple_tag
def getCount(request,value):
	gethelp = GetHelp.objects.filter(user_account=request.user)
	providehelp = ProvideHelp.objects.filter(user_account=request.user)
	if value == 'pending':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,confirmed=False)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,confirmed=False)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))
		get_count = req_obj_ph | req_obj_gh
		return get_count.count()

	
	elif value == 'completed':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,confirmed=True)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,confirmed=True)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))
		get_count = req_obj_ph | req_obj_gh
		return get_count.count()


	elif value == 'all':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))
		get_count = req_obj_ph | req_obj_gh
		return get_count.count()


	else:
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,deleted=True)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,deleted=True)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))
		get_count = req_obj_ph | req_obj_gh
		return get_count.count()


@register.simple_tag
def get_message_count(request,value):
	get_match_obj = MatchParticipants.objects.get(pk=value)
	all_messages = get_match_obj.get_all_messages_count()
	# print "all messages: ",all_messages
	if all_messages == None:
		return 0
	else:
		return all_messages


@register.simple_tag
def check_last_comment(request,value):
	get_match_obj = MessageCenterComment.objects.get(pk=value)
	all_comments = get_match_obj.get_comments()
	# print all_comments
	last_comment = all_comments[len(all_comments)-1]
	if last_comment.user.is_staff: 
		return "New Message"
	else:
		return all_comments.count()


@register.simple_tag
def get_user_messages(request,value):
	get_user_obj = UserAccount.objects.get(pk=value)
	all_messages = get_user_obj.user.messagecentercomment_set.all().count()
	# print all_messages
	return all_messages



@register.simple_tag
def get_all_users():
	return UserAccount.objects.all().count()


@register.simple_tag
def check_last_comment_admin(request,value):
	get_match_obj = MessageCenterComment.objects.get(pk=value)
	all_comments = get_match_obj.get_comments()
	# print all_comments
	last_comment = all_comments[len(all_comments)-1]
	if not last_comment.user.is_staff: 
		return "New Message"
	else:
		return all_comments.count()



@register.simple_tag
def check_last_comment_users_admin(request,value):
	get_match_obj = MatchParticipants.objects.get(pk=value)
	all_comments = get_match_obj.messagecentercomment.get_comments()
	# print all_comments
	last_comment = all_comments[len(all_comments)-1]
	if not last_comment.user.is_staff: 
		if last_comment.user == request.user:
			return all_comments.count()
		else:
			return 'New message'
	else:
		return 'New message'




