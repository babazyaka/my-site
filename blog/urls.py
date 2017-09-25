from django.conf.urls import url
from . import views
from django.contrib.flatpages import views as flatpage_view


urlpatterns = [
    # post views
    url(r'^$', views.post_list, name='post_list'),
    url(r'^contact/$', views.contact_form, name='contact'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.post_list, name='post_list_by_tag'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'
        r'(?P<post>[-\w]+)/$',
        views.post_detail,
        name='post_detail'),
    url(r'^about/$', flatpage_view.flatpage, {'url': '/about/'}, name='about'),

]
