from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.files.base import ContentFile
from base64 import b64decode
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core import serializers, mail
from django.db.models import Q, Count, Sum
from django.utils.text import Truncator
from django.contrib import messages
from django.template.context import RequestContext
from client.models import *
from django import template

import re
import hashlib
import datetime
import urllib
import time
import json, random, string
from django.core.urlresolvers import reverse
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from general.models import UserAccount
from django.core.mail import send_mail, EmailMessage, get_connection, EmailMultiAlternatives
from matchingApp.models import *
from matchingApp.forms import *
from client.views import getcontribNumber
from lvtvguinea.settings import EMAIL_HOST_USER
from general.views import send_msg, send_gh_msg, send_ph_msg



# Create your views here.



@login_required
@csrf_exempt
def create_match(request):

	context = {}
	template_name = 'lvtvAdmin_snippets/avail_ph.html'
	rp = request.POST
	print 'rp: ',rp
	ph_tracking_number = str(rp.get('adminSelectedPH'))
	gh_tracking_number = str(rp.get('adminSelectedGH'))
	ph_obj = ProvideHelp.objects.get(tracking_number=ph_tracking_number)
	ph_obj_email = str(ph_obj.user_account.email)
	user_obj = ph_obj.user_account
	gh_obj = GetHelp.objects.get(tracking_number=gh_tracking_number)
	gh_obj_email = str(gh_obj.user_account.email)
	amount = gh_obj.amount
	new_amount = ph_obj.amount
	amt_matched = 0.0

	if float(ph_obj.amount) > float(gh_obj.amount):
		if ph_obj.amt_left == 0.0 and gh_obj.amt_left == 0.0:
			print "a1"
			gh_obj.amt_paired = gh_obj.amount
			gh_obj.amt_left = 0.0
			gh_obj.status = "Paired"
			gh_obj.paired = True
			ph_obj.amt_paired = gh_obj.amount
			ph_obj.amt_left = float(ph_obj.amount) - float(gh_obj.amount)
			ph_obj.status = "Pairing"
			amt_matched = gh_obj.amount

		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left == 0.0:
			print "a2"
			if float(ph_obj.amt_left) > float(gh_obj.amount):
				print "a2.1"
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.amt_left = 0.0
				gh_obj.status = "Paired"
				gh_obj.paired = True
				ph_obj.amt_paired = float(ph_obj.amt_paired) + float(gh_obj.amount)
				ph_obj.amt_left = float(ph_obj.amt_left) - float(gh_obj.amount)
				ph_obj.status = "Pairing"
				amt_matched = gh_obj.amount
			elif float(ph_obj.amt_left) < float(gh_obj.amount):
				print "a2.2"
				gh_obj.amt_paired = ph_obj.amt_left
				gh_obj.amt_left = float(gh_obj.amount) - float(ph_obj.amt_left)
				gh_obj.status = "Pairing"
				amt_matched = ph_obj.amt_left
				ph_obj.amt_left = 0.0	
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				gh_obj.paired = False			
			else:
				print "a2.3"
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.amt_left = 0.0
				gh_obj.status = "Paired"
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.amt_left = 0.0
				ph_obj.status = "Paired"
				amt_matched = gh_obj.amount
				gh_obj.paired = True
				ph_obj.paired = True

		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left > 0.0:
			print "a3"
			if float(gh_obj.amt_left) > float(ph_obj.amt_left):
				print "a3.1"
				gh_obj.amt_left = float(gh_obj.amt_left) - float(ph_obj.amt_left)
				gh_obj.amt_paired = float(gh_obj.amt_paired) + float(ph_obj.amt_left) 
				gh_obj.status = "Pairing"
				ph_obj.status = "Paired"
				ph.amt_paired = ph_obj.amount
				amt_matched = ph_obj.amt_left
				ph_obj.amt_left = 0.0
				ph_obj.paired = True
				
			elif gh_obj.amt_left == ph_obj.amt_left:
				print "a3.2"
				gh_obj.amt_paired = ph_obj.amt_left
				gh_obj.status = "Paired"
				ph_obj.status = "Paired"
				ph.amt_paired = ph_obj.amt_left
				ph_obj.amt_left = 0.0
				ph_obj.paired = True
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0

			else:
				print "a3.3"
				ph_obj.amt_left = float(ph_obj.amt_left) - float(gh_obj.amt_left)
				gh_obj.amt_paired = gh_obj.amount
				ph_obj.amt_paired = float(ph_obj.amt_paired) + float(gh_obj.amt_left)
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
				gh_obj.status = "Paired"
				ph_obj.status = "Pairing"
				gh_obj.paired = True

		elif ph_obj.amt_left == 0.0 and gh_obj.amt_left > 0.0:
			print "a4"
			ph_obj.amt_left = float(ph_obj.amount) - float(gh_obj.amt_left)
			ph_obj.amt_paired = gh_obj.amt_left
			gh_obj.amt_paired = gh_obj.amount	
			gh_obj.status = "Paired"
			ph_obj.status = "Pairing"
			gh_obj.paired = True
			amt_matched = gh_obj.amt_left 
			gh_obj.amt_left = 0.0

	elif float(ph_obj.amount) < float(gh_obj.amount):
		if ph_obj.amt_left == 0.0 and gh_obj.amt_left == 0.0:
			print "B1"
			gh_obj.amt_left = float(gh_obj.amount) - float(ph_obj.amount)
			gh_obj.amt_paired = ph_obj.amount
			gh_obj.status = "Pairing"
			ph_obj.amt_left = 0.0
			ph_obj.amt_paired = ph_obj.amount
			ph_obj.status = "Paired"
			ph_obj.paired = True
			amt_matched = ph_obj.amount
		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left == 0.0:
			print "B2"
			if float(ph_obj.amt_left) > float(gh_obj.amount):
				print "b2.1"
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.status = "Paired"
				ph_obj.amt_left = float(ph_obj.amt_left) - float(gh_obj.amount)
				ph_obj.amt_paired = float(ph_obj.amt_paired) + float(gh_obj.amount)
				ph_obj.status = "Pairing"
				gh_obj.paired = True
				amt_matched = gh_obj.amount
			elif float(ph_obj.amt_left) < float(gh_obj.amount):
				print "b2.2"
				gh_obj.amt_left = float(gh_obj.amount) - float(ph_obj.amt_left)
				gh_obj.amt_paired = ph_obj.amt_left
				gh_obj.status = "Pairing"
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				amt_matched = ph_obj.amt_left
				ph_obj.amt_left = 0.0
			else:
				print "b2.3"
				gh_obj.amt_left = 0.0
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.status = "Paired"
				ph_obj.amt_left = 0.0
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				amt_matched = gh_obj.amount
				
		
		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left > 0.0:
			print "B3"
			if ph_obj.amt_left > gh_obj.amt_left:
				print "b3.1"
				gh_obj.status = "Paired"
				gh_obj.amt_paired = gh_obj.amount
				ph_obj.amt_left = float(ph_obj.amt_left) - float(gh_obj.amt_left)
				ph_obj.amt_paired = float(ph_obj.amt_paired) + float(gh_obj.amt_left)
				ph_obj.status = "Pairing"
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
			elif ph_obj.amt_left < gh_obj.amt_left:
				print "b3.2"
				gh_obj.amt_left = float(gh_obj.amt_left) - float(ph_obj.amt_left)
				gh_obj.status = "Pairing"
				gh_obj.amt_paired = float(gh_obj.amt_paired) + float(ph_obj.amt_left)
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				amt_matched = ph_obj.amt_left
				ph_obj.amt_left = 0.0
			else:
				print "b3.3"
				gh_obj.status = "Paired"
				gh_obj.amt_paired = gh_obj.amount
				ph_obj.amt_left = 0.0
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0

		elif ph_obj.amt_left == 0.0 and gh_obj.amt_left > 0.0:
			print "B4"
			if float(ph_obj.amount) > float(gh_obj.amt_left):
				print "b4.1"
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.status = "Paired"
				ph_obj.amt_left = float(ph_obj.amount) - float(gh_obj.amt_left)
				ph_obj.amt_paired = gh_obj.amt_left
				ph_obj.status = "Pairing"
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
			elif float(ph_obj.amount) < float(gh_obj.amt_left):
				print "b4.2"
				gh_obj.amt_left = float(gh_obj.amt_left) - float(ph_obj.amount)
				gh_obj.amt_paired = float(gh_obj.amt_paired) + float(ph_obj.amount)
				gh_obj.status = "Pairing"
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				amt_matched = ph_obj.amount
				ph_obj.amt_left = 0.0
			else:
				print "b4.3"
				gh_obj.amt_paired = gh_obj.amount
				gh_obj.status = "Paired"
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
				ph_obj.amt_left = 0.0

	else:
		if ph_obj.amt_left == 0.0 and gh_obj.amt_left == 0.0:
			print "c1"
			gh_obj.status = "Paired"
			gh_obj.amt_paired = gh_obj.amount		
			ph_obj.amt_paired = ph_obj.amount
			ph_obj.status = "Paired"
			gh_obj.paired = True
			ph_obj.paired = Tru
			amt_matched = gh_obj.amount
			ph_obj.amt_left = 0.0
			gh_obj.amt_left = 0.0

		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left == 0.0:
			print "c1"
			gh_obj.amt_left = float(gh_obj.amount) - float(ph_obj.amt_left)
			gh_obj.status = "Pairing"
			gh_obj.amt_paired = ph_obj.amt_left
			ph_obj.amt_paired = ph_obj.amount
			ph_obj.status = "Paired"
			ph_obj.paired = Tru
			amt_matched = ph_obj.amt_left
			ph_obj.amt_left = 0.0

		elif ph_obj.amt_left > 0.0 and gh_obj.amt_left > 0.0:
			print "c3"
			if ph_obj.amt_left > gh_obj.amt_left:
				print "c3.1"
				gh_obj.status = "Paired"
				gh_obj.amt_paired = gh_obj.amount
				ph_obj.amt_left = float(ph_obj.amt_left) - float(gh_obj.amt_left)
				ph_obj.amt_paired = float(ph_obj.amt_paired) + float(gh_obj.amt_left)
				ph_obj.status = "Pairing"
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
			elif ph_obj.amt_left == gh_obj.amt_left:
				print "c3.2"
				gh_obj.status = "Paired"
				gh_obj.amt_paired = gh_obj.amount
				ph_obj.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				gh_obj.paired = True
				amt_matched = gh_obj.amt_left
				gh_obj.amt_left = 0.0
				ph_obj.amt_left = 0.0
			else:
				print "c3.3"
				gh_obj.amt_left = float(gh_obj.amt_left) - float(ph_obj.amt_left)
				gh_obj.status = "Pairing"
				gh_obj.amt_paired = float(gh_obj.amt_paired) + float(ph_obj.amt_left)
				ph.amt_paired = ph_obj.amount
				ph_obj.status = "Paired"
				ph_obj.paired = True
				amt_matched = ph_obj.amt_left
				ph_obj.amt_left = 0.0

		elif ph_obj.amt_left == 0.0 and gh_obj.amt_left > 0.0:
			print "c4"
			gh_obj.status = "Paired"
			gh_obj.amt_paired = gh_obj.amount
			ph_obj.amt_paired = float(ph_obj.amount) - float(gh_obj.amt_left)
			ph_obj.status = "Pairing"
			gh_obj.paired = True
			amt_matched = gh_obj.amt_left
			gh_obj.amt_left = 0.0

	print "matched amount: ",amt_matched
	match_obj = MatchParticipants.objects.create(
		user=request.user,
		providehelp=ph_obj,
		gethelp=gh_obj,
		receiver=gh_obj.user_account,
		giver=ph_obj.user_account,
		amount_paired=gh_obj.amount,
		amt_matched=amt_matched,
		paired=True)

	ph_obj.save()
	gh_obj.save()

	try:
		subject = "Provide help"
		from_mail = EMAIL_HOST_USER
		to = ph_obj_email
		message = "You have been paired to provide help to the tune of GNF" + match_obj.amt_matched + "." + " Please log on to your account page for details"
		try:
			send_gh_msg(request,subject,message,from_mail,to)
		except:
			pass
	except Exception as e:
		print 'reg email error: ',e
		pass
	
	try:
		subject = "Get help"
		from_mail = EMAIL_HOST_USER
		to = gh_obj_email
		message = "You have been paired to get help to the tune of GNF" + match_obj.amt_matched + "." + " Please log on to your account page for details"
		try:
			send_ph_msg(request,subject,message,from_mail,to)
		except:
			pass
	except Exception as e:
		print 'reg email error: ',e
		pass

	print "i am here finally B"	
	providehelp = ProvideHelp.objects.filter((~Q(user_account = user_obj)))
	context['providehelp'] = providehelp
	return render(request,template_name,context)



@login_required
def paid_received(request):
	rp = request.POST
	print rp
	response = redirect(request.META['HTTP_REFERER'])
	match_obj = MatchParticipants.objects.get(pk=rp.get('match_id'))
	if rp.get('paid_received') == "paid":
		match_obj.payment_made = True
		match_obj.confirmation_image = request.FILES.get('pay_file')
		gh_obj = match_obj.gethelp
		gh_obj.payment_made = True
		gh_obj.save()
		print "success here"
	else:
		match_obj.payment_received = True
		match_obj.confirmed = True
		ph_obj = match_obj.providehelp
		gh_obj = match_obj.gethelp
		gh_obj.completed = True
		if float(ph_obj.amount) == float(ph_obj.amt_paired):
			print "True"
			ph_obj.help_provided = True
		else:
			print "False"
			ph_obj.help_provided = False

		ph_obj.save()
		gh_obj.save()


		if not gh_obj.rel_to == "referral" and not ph_obj.user_account.useraccount.referral == None: 
			get_ref_email = str(ph_obj.user_account.useraccount.referral)
			user_obj = User.objects.get(email=get_ref_email.strip())
			tracking_number = getcontribNumber('GH')
			amount = float(0.01) * float(match_obj.amt_matched)
			get_help_obj = GetHelp.objects.create(
				getHelp=True,
				user_account=user_obj,
				tracking_number=tracking_number,
				tAndC = True,
				rel_to = 'referral',
				amount=amount,
				created_on=datetime.datetime.now())
		else:
			pass

		# print user_acc_obj
		print "success there"

	match_obj.save()
	return response



@login_required
@csrf_exempt
def get_comments(request):
	context = {}
	if request.method == 'POST':
		print "see me here"
		rp = request.POST
		print "rp: ", rp
		match_obj = MatchParticipants.objects.get(pk=rp.get('match_message_id'))
		msg_obj,created = MessageCenterComment.objects.get_or_create(matches=match_obj)
		comment_obj = Comment.objects.create(
				message=rp.get('message'),
				message_obj=msg_obj,
				image_obj=request.FILES.get('image_obj'),
				user=request.user)
		print msg_obj.get_comments()
		print "see me again"
		context['matched_order'] = match_obj
		messages.success(request,'Message sent successfully')
		return redirect(request.META['HTTP_REFERER'])
	else:
		form = CommentForm()
		rg = request.GET
		print "see me there"
		print "rg: ", rg
		match_obj = MatchParticipants.objects.get(pk=rg.get('pk'))
		context['matched_order'] = match_obj
		context['form'] = form
		return render(request, 'matchingApp_snippets/comments.html', context)



@login_required
@csrf_exempt
def supoort_messages(request):
	context = {}
	if request.method == 'POST':
		rp = request.POST
		print "rp: ", rp
		if not rp.has_key('support'):
			message_obj = MessageCenterComment.objects.create(
				subject=rp.get('subject'),
				message=rp.get('message'),
				user=request.user,
				image_obj=request.FILES.get('file_obj'),
				)
			message_obj.admin = True
			message_obj.save()
			comment_obj = Comment.objects.create(
				message=rp.get('message'),
				message_obj=message_obj,
				user=request.user)
			messages.success(request,'Message sent successfully')
			return redirect(request.META['HTTP_REFERER'])
		else:
			print "way"
			message_obj = MessageCenterComment.objects.get(pk=rp.get('msg_id'))
			comment_obj = Comment.objects.create(
				message=rp.get('message'),
				message_obj=message_obj,
				image_obj = request.FILES.get('image_obj'),
				user=request.user)
			context['message_obj'] = message_obj
			messages.success(request,'Message sent successfully')
			return redirect(request.META['HTTP_REFERER'])
	else:
		rg = request.GET
		form = CommentForm()
		print "see me over here"
		print "rg: ", rg
		message_obj = MessageCenterComment.objects.get(pk=rg.get('pk'))
		context['message_obj'] = message_obj
		context['form'] = form
		return render(request, 'lvtvAdmin_snippets/support_comments.html', context)



























