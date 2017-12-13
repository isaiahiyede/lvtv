from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse , HttpResponseRedirect, JsonResponse
from django.forms.models import model_to_dict
from django.contrib.auth.decorators import user_passes_test
from general.models import *
from client.models import *
from general.forms import UserForm, UserAccountForm, LoginForm
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.models import User
from itertools import chain
from operator import attrgetter
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
from django.template.context import RequestContext
from django.db.models import Count
from django import template
from itertools import chain
import re
import hashlib
import random, datetime
import urllib
import time
from django.core.urlresolvers import reverse
import json
from django.db.models import Sum
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage, send_mail
from matchingApp.models import MessageCenterComment
from lvtvAdmin.views import paginate_list
from lvtvguinea.settings import EMAIL_HOST_USER


# Create your views here.


def send_gh_msg(request,subject,message,from_mail,to):
	message = message
	subject = subject
	to = [to]
	msg = EmailMessage(subject, message, from_mail, to)
	msg.send()
	return HttpResponse(message)


def send_ph_msg(request,subject,message,from_mail,to):
	message = message
	subject = subject
	to = [to]
	msg = EmailMessage(subject, message, from_mail, to)
	msg.send()
	return HttpResponse(message)


def send_msg(request,subject,message,from_mail,to,email,template_name):
	template_name = 'base/' + template_name + '.html'
	message = message
	subject = subject
	to = [to]
	ctx  = {
		'body': message,
		'email': email,
		}
	message = get_template('base/contact_support.html').render(Context(ctx))
	msg = EmailMessage(subject, message, from_mail, to)
	msg.send()
	return HttpResponse(message)


def homepage(request):
	context = {}
	template_name = 'general/index.html'
	get_user_test = Testimonials.objects.all()
	context['testimonials'] = get_user_test
	return render(request, template_name, context)


def userlogin(request):
	context = {}
	username  = ""
	context['login_form'] = LoginForm()

	if request.method == "POST":
	    form = LoginForm(data = request.POST)

	    if form.is_valid:
	        email    = request.POST.get('email').strip()
	        password = request.POST.get('password').strip()
	        
	        user_account =  User.objects.filter((Q(email= email) | Q(useraccount__phone_number=email)))
	        
	        if not user_account.exists():
				context['email_not_found'] = True
				context['email'] = email
				return render(request, 'general/login.html', context )

	        if user_account.exists():
	            username = user_account[0].username
	        auth_user = authenticate(username = username, password = password)

	        if auth_user is not None:
	            user = auth_user

	            if user.is_active:
	                login(request, user)                    

	                if user.is_staff:
	                    response =  redirect(reverse('lvtvAdmin:admin_views'))
	                    return response
	                   
	                else:
	                    response = redirect(reverse("client:client_views"))
	                    return response
	        else:
	            # print "No details found for %s" %(email)
	            context['no_record_found'] = True
	        return render(request, 'general/login.html', context )
	else:
		return render(request, 'general/login.html',context)
	context = {}
	template_name = 'general/login.html'
	return render(request, template_name, context)


def userregister(request):
	print "Got here"
	context = {}	
	
	user_form = UserForm()
	user_account_form = UserAccountForm()

	context['user_form'] = user_form
	context['user_account_form'] = user_account_form

	if  request.method            ==     "POST":
	    rp                         =     request.POST
	    # print "rp:",rp	        
        userform                   =     UserForm(request.POST)
        user_account_form          =     UserAccountForm(request.POST)
        print "here1"
        # print userform.first_name
        check_ref_email = User.objects.filter(email=rp.get('referral'))
        if not check_ref_email.exists():
        	referral = rp.get('referral')
        	return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'referral_email_not_exists':True,'referral':referral})
        elif check_ref_email[0].is_staff:
        	referral = rp.get('referral')
        	return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'referral_denied':True,'referral':referral})
        if rp.get('email') == rp.get('referral'):
			referral = rp.get('referral')
			return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'referral_and_email_same':True,'referral':referral})			
        if User.objects.filter(username = rp.get('username')).exists():                
            return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'username_is_taken':True})
        if User.objects.filter(email = rp.get('email')).exists():                
            return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'email_is_taken':True})
        if UserAccount.objects.filter(phone_number = rp.get('phone_number')).exists():
            return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'phone_is_taken':True})
        else:
			print "here2"
			if userform.is_valid and user_account_form.is_valid:
				print "here3"
				password1     = rp.get('password')
				password2     = rp.get('confirm_password')
				if password1 != password2:
					return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_mismatch':True})
				if len(password1) < 6:
					return render(request, 'general/register.html', {'user_form':userform, 'user_account_form':user_account_form,'password_too_short':True})
				user = User.objects.create(username = rp.get('username'), email = rp.get('email').lower(),
					first_name = rp.get('first_name'), last_name = rp.get('last_name'))
				user.set_password(rp.get('password')) 
				user.save()
				print 'here4'
				new_user_account = UserAccount.objects.create(
					user = user,
					phone_number = rp.get('phone_number'),
					created_on   = datetime.datetime.now())
				print 'here5'
				new_referral = Referrals.objects.create(user=new_user_account,email=rp.get('referral'))
				context['user_is_created']  =    True
				context['email']            =    rp.get('email')
				print "user creation for %s successful" %(user)
				return redirect(reverse('general:successful_registration'))
			else:
				print "errors detected"                    
				return render(request, 'general/register.html', context)  

        return redirect(request.META['HTTP_REFERER'])
	return render(request, 'general/register.html',context)


def gen_views(request,action):
	context = {}
	action  = str(action)
	print action
	if action == "testimonials":
		get_user_test = Testimonials.objects.all()
		context['testimonials'] = get_user_test
	elif action == "register":
		user_form = UserForm
		user_account_form = UserAccountForm
		context['user_form'] = user_form
		context['user_account_form'] = user_account_form
	template_name = 'general' + '/' + action + '.html'
	return render(request, template_name, context)


def successful_registration(request):
    context = {}    
    return render(request, 'general/successfulReg.html', context)


@login_required
def referrals(request):
    context = {} 
    get_user = UserAccount.objects.get(user=request.user)
    get_refs = get_user.get_refs()
    get_all_refs = paginate_list(request, get_refs, 10)  
    context['referrals'] = get_all_refs
    return render(request, 'general/referrals.html', context)


def user_logout(request):
	response = redirect(reverse('general:homepage'))
	logout(request)
	return response


@login_required
def update_profile(request):
	print 'got here'
	response = redirect(reverse('client:client_views'))
	user_obj = request.user
	user_obj.useraccount.title = request.POST.get('title')
	user_obj.useraccount.bank_name = request.POST.get('bank_name')
	user_obj.useraccount.bank_acc_number = request.POST.get('bank_acc_number')
	user_obj.useraccount.updated_on = datetime.datetime.now()
	user_obj.useraccount.completed = True
	user_obj.useraccount.profile_up_to_date = True
	user_obj.useraccount.save()
	return response


@login_required
def delete_item(request,description,item_id):
	pk = item_id
	msg_obj = MessageCenterComment.objects.get(pk=pk)
	msg_obj.deleted = True
	msg_obj.save()
	return redirect(request.META['HTTP_REFERER'])


def contact_support(request):
	to = EMAIL_HOST_USER
	rp = request.POST
	from_email = '{} <{}>'.format('lvtv', 'info@adisenergy.com')
	try:
		send_msg(request, rp.get('subject'), rp.get('message'), from_email, to, rp.get('email'))
	except:
		pass
	return redirect(request.META['HTTP_REFERER'])

























