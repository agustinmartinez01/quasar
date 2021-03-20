from django.conf.urls import url
from Space import views


space_detail = views.SpaceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
})
space_list = views.SpaceViewSet.as_view({
    'post': 'create',
    'get': 'list',
})

urlpatterns = [
    url(r'^satelite/$', space_list, name='space_list'),
    url(r'^satelite/(?P<id>[0-9]+)/$', space_detail, name='space_detail'),
    url(r'^topsecret/$', views.TopSecret.as_view(), name='topsecret'),
    url(r'^topsecret_split/(?P<string>[\w\-]+)', views.TopSecretSplit.as_view(), name='topsecret_get'),
    url(r'^topsecret_split/$', views.TopSecretSplit.as_view(), name='topsecret_post'),

]