from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [

			url(r'^get/orders/$', views.admin_views,  name="admin_views"),
			url(r'^gh-pair/$', views.get_gh_pair,  name="get_gh_pair"),
			url(r'^get-users/$', views.get_users,  name="get_users"),
			url(r'^get-messages/$', views.get_messages,  name="messages"),
			url(r'^user-action/$', views.user_actions,  name="user_action"),
			url(r'^user-edit/$', views.user_edit,  name="user_edit"),
			url(r'^providehelp/$', views.get_phs,  name="get_phs"),
			url(r'^get-details-gh/$', views.get_details_gh,  name="get_details_gh"),
			url(r'^message/center/$', views.admin_messages,  name="admin_messages"),
			url(r'^message/center/admin$', views.get_admin_msgs,  name="get_admin_msgs"),
        ]