from django.conf.urls import patterns, include, url
from django.conf import settings
import views


urlpatterns = [
			url(r'^orders-count/(?P<attribute>[-\w]+)/$', views.orders_count, name="orders_count"),
            url(r'^contrib/$', views.create_contrib, name="create_contrib"),
            url(r'^account-standing/$', views.account_page, name="account_page"),
            url(r'^delete-item/(?P<tracking_number>.+)/$', views.del_request, name="del_request"),
            url(r'^get-details/$', views.get_details, name="get_details"),
            url(r'^client-page/$', views.client_views, name="client_views"),
            url(r'^support/$', views.client_support, name="client_support"),
            url(r'^client-testimonial/$', views.testimonial, name="testimonial"),

        ]