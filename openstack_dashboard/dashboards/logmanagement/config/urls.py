from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.logmanagement.config import views 


urlpatterns = patterns(
    '',
    url(r'^$', views.IndexView.as_view(), name='index'),
)
