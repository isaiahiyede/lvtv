from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [
			url(r'^create-match/$', views.create_match, name="create_match"),
			url(r'^paid-for/$', views.paid_received, name="paid_received"),
			url(r'^get_comments/$', views.get_comments, name="get_comments"),
			url(r'^supoort_messages/$', views.supoort_messages, name="supoort_messages"),

        ]


        