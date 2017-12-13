from django.shortcuts import render
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

from django import template

import re
import hashlib
import datetime
import urllib
import time
import json, random

from django.core.urlresolvers import reverse

from django.template.loader import get_template, render_to_string
from django.template import Context
from django.utils import timezone

from django.core.serializers.json import DjangoJSONEncoder
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import send_mail, EmailMessage,  get_connection, EmailMultiAlternatives
from client.models import ProvideHelp, GetHelp
from general.models import UserAccount
from matchingApp.models import *
from matchingApp.forms import *



# Create your views here.

def paginate_list(request, objects_list, num_per_page):
    paginator   =   Paginator(objects_list, num_per_page) # show number of jobs per page
    page  = request.GET.get('page')
    try:
        paginated_list  = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an integer, deliver first page
        paginated_list   =   paginator.page(1)
    except  EmptyPage:
        #if page is out of range(e.g 9999), deliver last page of results
        paginated_list      =   paginator.page(paginator.num_pages)
    return paginated_list



@login_required
def admin_views(request):
	context = {}
	gethelp = GetHelp.objects.all()
	providehelp = ProvideHelp.objects.all()
	ghsum = gethelp.aggregate(Sum('amount'))['amount__sum']
	phsum = providehelp.aggregate(Sum('amount'))['amount__sum']
	greater_of_gh_ph = ''
	if ghsum > phsum:
		greater_of_gh_ph = False
	elif ghsum > phsum:
		greater_of_gh_ph = True
	else:
		greater_of_gh_ph = True
	context['greater_of_gh_ph'] = greater_of_gh_ph
	all_contribs = list(reversed(sorted(chain(gethelp, providehelp), key=attrgetter('created_on'))))
	contribs = paginate_list(request,all_contribs,10)
	context['contributions'] = contribs
	context['phsum'] = phsum
	context['ghsum'] = ghsum
	template_name = 'lvtvAdmin/lvtvAdmin.html'
	return render(request, template_name, context)



@login_required
def get_gh_pair(request):
	context = {}
	tracking_number = request.GET.get('tracking_number')
	gethelp = GetHelp.objects.get(tracking_number=tracking_number)
	user_obj = gethelp.user_account
	providehelp = ProvideHelp.objects.filter((~Q(user_account = user_obj)),(~Q(paired=True)),(~Q(status="Paired")))
	context['providehelp'] = providehelp
	return render(request, 'lvtvAdmin_snippets/avail_ph.html', context)



@login_required
def get_phs(request):
	context = {}
	tracking_number = request.GET.get('tracking_number')
	ph = ProvideHelp.objects.get(tracking_number=tracking_number)
	user_obj = ph.user_account
	providehelp = ProvideHelp.objects.filter((~Q(user_account = user_obj)),(~Q(paired=True)),(~Q(status="Paired")))
	print providehelp
	context['tracking_number'] = tracking_number
	context['providehelp'] = providehelp
	return render(request, 'lvtvAdmin_snippets/avail_ph.html', context)



@login_required
def	get_details_gh(request):
	context = {}
	gh_type = request.GET.get('gh_type')
	if gh_type == "allPhPaired":
		gethelp = ProvideHelp.objects.filter(paired=True)
		gh_header = "All paired provide help request"
		get_help = True
		is_paired = True
	elif gh_type == "allGhPaired":
		is_paired = True
		gethelp = GetHelp.objects.filter(paired=True)
		gh_header = "All paired get help request"
		get_help = True
	elif gh_type == "allGhPairedUnpaired":
		is_paired = False
		gethelp = GetHelp.objects.filter(paired=False)
		gh_header = "All unpaired get help request"
		get_help = False
	elif gh_type == "allPhPairedUnpaired":
		is_paired = False
		gethelp = ProvideHelp.objects.filter(paired=False)
		gh_header = "All unpaired provide help request"
		get_help = False
	else:
		print "Gh against Ph Indicator"
		ph_total_1 = ProvideHelp.objects.filter(paired=False).aggregate(Sum('amount'))['amount__sum']
		ph_total_2 = ProvideHelp.objects.filter(status="Pairing").aggregate(Sum('amt_paired'))['amt_paired__sum']
		if ph_total_1 == None:
			ph_total_1 = 0.0
		if ph_total_2 == None:
			ph_total_2 = 0.0

		ph_total = ph_total_1 - ph_total_2

		gh_total_1 = GetHelp.objects.filter(paired=False,status="Pairing").aggregate(Sum('amount'))['amount__sum']
		gh_total_2 = GetHelp.objects.filter(status="Pairing").aggregate(Sum('amt_paired'))['amt_paired__sum']
		if gh_total_1 == None:
			gh_total_1 = 0.0
		if gh_total_2 == None:
			gh_total_2 = 0.0

		gh_total = gh_total_1 - gh_total_2

		indicator_message = ''
		if gh_total == 0.0:
			gh_total = 0.0
		if ph_total == 0.0:
			ph_total = 0.0
		if ph_total >= gh_total:
			indicator_message = "System OK"
		else:
			indicator_message = "System NOT OK"

		context['indicator_message'] = indicator_message
		context['gethelp'] = gh_total
		context['providehelp'] = ph_total
		return render(request, 'lvtvAdmin_snippets/gh_ph_indicator.html', context)
	context['gethelp'] = gethelp
	context['gh_header'] = gh_header
	context['get_help'] = get_help
	context['is_paired'] = is_paired
	return render(request, 'lvtvAdmin_snippets/gh_type_values.html', context)



@login_required
def get_users(request):
	context = {}
	template_name = 'lvtvAdmin/users.html'
	user_account = UserAccount.objects.all()
	user_objs = paginate_list(request,user_account,10)
	context['user_account'] = user_objs
	return render(request,template_name,context)



@login_required
def get_messages(request):
	context = {}
	template_name = 'lvtvAdmin/messages.html'
	user_account = UserAccount.objects.all()
	user_objs = paginate_list(request,user_account,10)
	context['user_account'] = user_objs
	return render(request,template_name,context)



@login_required
def user_actions(request):
	context = {}
	rg = request.GET
	# print rg
	action = rg.get('action')
	user_obj = UserAccount.objects.get(pk=rg.get('pk'))
	context['user'] = user_obj
	template_name = 'lvtvAdmin_snippets' + '/' + action + '.html'
	return render(request, template_name, context)



@login_required
def user_edit(request):
	context = {}	
	if request.method == 'POST':
		rp = request.POST
		# print rp
		useracc_obj = UserAccount.objects.get(pk=rp.get('user_id'))
		useracc_obj.phone_number = rp.get('phone_num')
		useracc_obj.bank_name = rp.get('bank_name')
		useracc_obj.bank_acc_number = rp.get('bank_acc_number')
		useracc_obj.save()

		user_obj = useracc_obj.user
		user_obj.first_name = rp.get('firstname')
		user_obj.last_name = rp.get('lastname')
		user_obj.username = rp.get('username')
		user_obj.email = rp.get('user_email')
		user_obj.save()

		return redirect(request.META['HTTP_REFERER'])
	else:
		user_obj = UserAccount.objects.get(pk=request.GET.get('pk'))
		context['user'] = user_obj
		template_name = 'lvtvAdmin_snippets/editprofile.html' 
		return render(request, template_name, context)


@login_required
def admin_messages(request):
	context = {}
	message_obj = MessageCenterComment.objects.filter(deleted=False)
	context['message_obj'] = message_obj
	template_name = 'lvtvAdmin/admin_messages.html'
	return render(request,template_name,context)



@login_required
@csrf_exempt
def get_admin_msgs(request):
	context = {}
	if request.method == 'POST':
		print "see admin here"
		rp = request.POST
		print "rp: ", rp
		if not rp.get('image') == "":
			image_obj = rp.get('image')
		else:
			image_obj =  ""
		msg_obj = MessageCenterComment.objects.get(pk=rp.get('admin_msg_id'))
		comment_obj = Comment.objects.create(
				message=rp.get('message'),
				message_obj=msg_obj,
				user=request.user,
				image_obj = request.FILES.get('image_obj'),
				support_admin=True)
		# print msg_obj.get_comments()
		print "see admin again"
		context['msg_obj'] = msg_obj
		messages.success(request,'Message sent successfully')
		return redirect(request.META['HTTP_REFERER'])
	else:
		form = CommentForm()
		rg = request.GET
		print "see admin there"
		print "rg: ", rg
		msg_obj = MessageCenterComment.objects.get(pk=rg.get('pk'))
		context['msg_obj'] = msg_obj
		context['form'] = form
		return render(request, 'lvtvAdmin_snippets/admin_msg_modal.html', context)



        






















	