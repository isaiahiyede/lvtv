from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [

            url(r'^$', views.homepage,  name="homepage"),
            url(r'^signup/Page/$', views.userregister,  name="userregister"),
            url(r'^login/Page/$', views.userlogin,  name="login"),
            url(r'^general-views/(?P<action>.+)$', views.gen_views, name="gen_views"),
            url(r'^logout/$', views.user_logout, name='user_logout'),
            url(r'^successful_registration/$', views.successful_registration, name='successful_registration'),
            url(r'^update_profile/$', views.update_profile, name='update_profile'),
            url(r'^clientRefs/$', views.referrals, name="referrals"),
            url(r'^supportContact/$', views.contact_support, name="contact_support"),
            url(r'^general/delete/(?P<description>.+)/(?P<item_id>[-\w]+)/$', views.delete_item, name='delete_item'),
	]