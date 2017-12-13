# -*- coding: utf-8 -*-
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
from client.forms import *
from client.models import *
from general.forms import UserAccountForm
from django import template
from general.views import send_msg, send_gh_msg, send_ph_msg

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
from django.utils.timezone import utc
from django.core.mail import send_mail, EmailMessage,  get_connection, EmailMultiAlternatives
from matchingApp.models import *
from lvtvAdmin.views import paginate_list
from lvtvguinea.settings import EMAIL_HOST_USER


# Create your views here.


def getcontribNumber(value):
	allowed_chars = ''.join((string.uppercase, string.digits))
	unique_id = ''.join(random.choice(allowed_chars) for _ in range(9))
	return value + unique_id



@login_required
def orders_count(request,attribute):
	context = {}
	phForm = ProvideHelpForm(request.POST)
	ghForm = GetHelpForm(request.POST)
	context['phform'] = phForm
	context['ghform'] = ghForm
	context['profileform'] = UserAccountForm()
	useraccount_obj = UserAccount.objects.get(user=request.user)
	context['useraccount_obj'] = useraccount_obj
	gethelp = GetHelp.objects.filter(user_account=request.user)
	providehelp = ProvideHelp.objects.filter(user_account=request.user)
	contribs = list(reversed(sorted(chain(gethelp, providehelp), key=attrgetter('created_on'))))
	current_time = datetime.datetime.utcnow().replace(tzinfo=utc)

	if attribute == 'pending':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,confirmed=False)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,confirmed=False)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))

	elif attribute == 'completed':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,confirmed=True)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,confirmed=True)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))

	elif attribute == 'all':
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))

	else:
		req_obj_gh 	= MatchParticipants.objects.filter(providehelp=providehelp,deleted=True)
		req_obj_ph 	= MatchParticipants.objects.filter(gethelp=gethelp,deleted=True)
		all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))

	req_obj = paginate_list(request, all_req_obj, 5)
	# print "the orders: ",all_req_obj
	context['contributions'] = contribs
	context['req_obj'] = req_obj
	context['current_time'] = current_time
	template_name = 'clients/clientpage.html'
	return render(request, template_name, context)



@login_required
def client_views(request):
	context = {}
	phForm = ProvideHelpForm(request.POST)
	ghForm = GetHelpForm(request.POST)
	context['phform'] = phForm
	context['ghform'] = ghForm
	context['profileform'] = UserAccountForm()
	useraccount_obj = UserAccount.objects.get(user=request.user)
	current_time = datetime.datetime.utcnow().replace(tzinfo=utc)

	context['useraccount_obj'] = useraccount_obj
	gethelp = GetHelp.objects.filter(user_account=request.user)
	providehelp = ProvideHelp.objects.filter(user_account=request.user)
	contribs = list(reversed(sorted(chain(gethelp, providehelp), key=attrgetter('created_on'))))

	req_obj_gh = MatchParticipants.objects.filter(providehelp=providehelp,confirmed=False,deleted=False)
	req_obj_ph = MatchParticipants.objects.filter(gethelp=gethelp,confirmed=False,deleted=False)
	all_req_obj = list(reversed(sorted(chain(req_obj_gh, req_obj_ph))))

	for requested_obj in all_req_obj:
		if requested_obj.confirmed == True:
			pass
		else:
			if requested_obj.giver == request.user:
				''' user who is supposed to pay does not pay at all '''
				if (requested_obj.payment_made == False) and (requested_obj.time_left_after_5_days() <= current_time):

					useraccount_obj = UserAccount.objects.get(user=request.user)
					useraccount_obj.block = True
					useraccount_obj.defaulter = True
					useraccount_obj.defaulter_msg = u"Vous avez refusé de faire des contours comme promis ... Par conséquent, votre compte a été bloqué jusqu'à nouvel ordre et vous avez perdu les bonus accumulés"
					useraccount_obj.save()
	
					ph_num_of_requested_obj = requested_obj.providehelp.tracking_number
					ph_of_requested_obj = ProvideHelp.objects.get(tracking_number=ph_num_of_requested_obj)
					ghs_of_ph_of_requested_obj = GetHelp.objects.filter(rel_to=ph_num_of_requested_obj)

					for gh_order in ghs_of_ph_of_requested_obj:
						if gh_order.payment_made:
							pass
						else:
							if gh_order.status == "Pairing":
								gh_order.status = "New"
								gh_order.rel_to = None
								gh_order.amt_paired = 0.0
								gh_order.amt_left = 0.0
							elif gh_order.status == "Paired":
								gh_order.status = "Pairing"
								gh_order.amt_paired = float(gh_order.amount) - float() 


					context['useraccount_obj'] = useraccount_obj
					requested_obj.deleted = True
				else:
					pass

			elif requested_obj.receiver == request.user:
				''' user who is supposed to confirm does not confirm payment at all '''
				if (requested_obj.payment_made == True) and (requested_obj.payment_received == False) and (requested_obj.time_left_after_5_days() <= current_time):
					useraccount_obj = UserAccount.objects.get(user=request.user)
					useraccount_obj.block = True
					useraccount_obj.defaulter_msg = u"La confirmation n'a pas été faite dans le délai stipulé ... À ce stade, si vous êtes sûr de ne pas avoir été payé, envoyez une copie scannée claire de votre relevé bancaire au cours des 21 derniers jours pour confirmation dans les 72 heures à venir. Si vous ne le faites pas, votre compte sera suspendu indéfiniment et tous les bonus seront perdus. Notez également que ces mesures strictes sont prises pour s'assurer que seules les personnes loyales et sérieuses bénéficient de ce grand programme"
					useraccount_obj.save()
		
					useraccount_obj2 = UserAccount.objects.get(user=requested_obj.giver)
					useraccount_obj.block = True
					useraccount_obj.defaulter_msg = u"La confirmation n'a pas été faite dans le délai stipulé ... À ce stade, si vous êtes sûr de faire un paiement, envoyez une copie scannée claire de votre relevé bancaire au cours des 21 derniers jours pour confirmation dans les 72 heures à venir. Si vous ne le faites pas, votre compte sera suspendu indéfiniment et tous les bonus seront perdus. Notez également que ces mesures strictes sont prises pour s'assurer que seules les personnes loyales et sérieuses bénéficient de ce grand programme"
					useraccount_obj.save()

					context['useraccount_obj'] = useraccount_obj
				else:
					pass

	req_obj= paginate_list(request, all_req_obj, 5)
	# print "the orders: ",all_req_obj
	context['contributions'] = contribs
	context['req_obj'] = req_obj
	context['current_time'] = current_time
	template_name = 'clients/clientpage.html'
	return render(request, template_name, context)



@login_required
def create_contrib(request):
	context = {}
	response = redirect(request.META['HTTP_REFERER'])

	if request.POST.has_key('providehelp'):
		tracking_number = getcontribNumber('PH')
	else:
		
		related_obj = ProvideHelp.objects.get(tracking_number=request.POST.get('ph_req'))
		related_obj.help_requested = True
		related_obj.rel_to = request.POST.get('ph_req')
		related_obj.amount_requested = float(request.POST.get('amount_req'))

		tracking_number = getcontribNumber('GH')

		get_help_obj = GetHelp.objects.create(
			getHelp=True,
			user_account=request.user,
			tracking_number=tracking_number,
			tAndC = True,
			rel_to = request.POST.get('ph_req'),
			amount=request.POST.get('amount_req'),
			created_on=datetime.datetime.now())

		subject = "Request to get help"
		to = EMAIL_HOST_USER
		from_mail = EMAIL_HOST_USER
		message = "GNF" + get_help_obj.amount + " request to get help created by" + " " + str(request.user.username) + " on" + " " + str(get_help_obj.created_on)
		try:
			send_gh_msg(request,subject,message,from_mail,to)
		except:
			pass

		related_obj.rel_to = get_help_obj.tracking_number
		related_obj.save()

		return response

	if request.method == "POST":
		form = ProvideHelpForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.provideHelp = True
			post.user_account = request.user
			post.tracking_number = tracking_number
			post.created_on = datetime.datetime.now()
			post.tAndC = True 
			post.save()

			subject = "Request to provide help"
			to = EMAIL_HOST_USER
			from_mail = EMAIL_HOST_USER
			message = "GNF" + post.amount + " request to provide help created by" + " " + str(request.user.username) + " on" + " " + str(post.created_on)
			try:
				send_ph_msg(request,subject,message,from_mail,to)
			except:
				pass

			return response
		else:
			print form.errors
	else:
		return response
	return response



@login_required
def account_page(request):
	context = {}
	gethelp = GetHelp.objects.filter(user_account=request.user)
	providehelp = ProvideHelp.objects.filter(user_account=request.user)
	all_contribs = list(reversed(sorted(chain(gethelp, providehelp), key=attrgetter('created_on'))))
	context['current_time_15days'] = datetime.datetime.utcnow().replace(tzinfo=utc) + timedelta(days=15)
	context['current_time_30days'] = datetime.datetime.utcnow().replace(tzinfo=utc) + timedelta(days=30) 
	current_time = datetime.datetime.utcnow().replace(tzinfo=utc)
	contribs= paginate_list(request, all_contribs, 10)  
	context['contributions'] = contribs
	context['current_time'] = current_time
	template_name = 'clients/accountStanding.html'
	return render(request,template_name,context)



@login_required
def del_request(request,tracking_number):
	response = redirect(request.META['HTTP_REFERER'])
	track_num = str(tracking_number)[0:2]
	if track_num == 'PH':
		rel_obj = ProvideHelp.objects.get(tracking_number=tracking_number)
		# print rel_obj.rel_to
		gh_obj = GetHelp.objects.filter(tracking_number=rel_obj.rel_to)
		# print gh_obj
		if gh_obj.exists():
			gh_obj.delete()
		else:
			pass
		rel_obj.delete()
	else:
		rel_obj = GetHelp.objects.get(tracking_number=tracking_number)
		ph_obj = ProvideHelp.objects.get(tracking_number=rel_obj.rel_to)
		ph_obj.help_requested = False
		ph_obj.amount_requested = ""
		ph_obj.rel_to = None
		ph_obj.save()
		rel_obj.delete()
	return response



@login_required
def get_details(request):
	context = {}
	rG = request.GET
	template_name = 'clients_snippets/matchedVal.html'
	if str(rG.get('tracking_number'))[0:2] == 'PH':
		req_obj = ProvideHelp.objects.get(tracking_number=rG.get('tracking_number'))
		context['req_obj'] = req_obj
	else:
		req_obj = GetHelp.objects.get(tracking_number=rG.get('tracking_number'))
		context['req_obj'] = req_obj
	response = render(request, template_name, context)
	return response



@login_required
def testimonial(request):
	response = redirect(request.META['HTTP_REFERER'])
	rp = request.POST
	print "rp:", rp
	if rp.get('test_image') != "":
		test_image = request.FILES.get('test_image')
	else:
		test_image = 'sample.doc'
	if str(rp.get('test_track_num'))[0:2] == 'PH':
		ph_help_obj = ProvideHelp.objects.get(tracking_number=rp.get('test_track_num'))
		default_message = "J'ai aide GNF " + ph_help_obj.amount + " et aide recue " + ph_help_obj.amount_requested
		testimonial_obj = Testimonials.objects.create(
		user=request.user, 
		message=rp.get('test_message'), 
		testimony_ph=ph_help_obj, 
		testimony_image = test_image,
		default_text=default_message)
		ph_help_obj.testimony = True
		ph_help_obj.save()
	else:
		gh_help_obj = GetHelp.objects.get(tracking_number=rp.get('test_track_num'))
		if not gh_help_obj.rel_to == "referral":
			ph_help_obj = ProvideHelp.objects.get(tracking_number=gh_help_obj.rel_to)
			help_provided = ph_help_obj.amount
			default_message = "J'ai aide of GNF " + help_provided + " et aide recue GNF " + gh_help_obj.amount
		else:
			default_message = "J'ai recu un bonus de recommandation de GNF " + gh_help_obj.amount
		testimonial_obj = Testimonials.objects.create(
		user=request.user, 
		message=rp.get('test_message'), 
		testimony_gh=gh_help_obj,
		testimony_image = test_image,
		default_text=default_message)
		gh_help_obj.testimony = True
		gh_help_obj.save()
		
	return response


@login_required
def client_support(request):
	context = {}
	message_obj = MessageCenterComment.objects.filter(user=request.user,admin=True)
	context['message_obj'] = message_obj
	response = render(request,'clients/admin_support.html',context)
	return response







			














