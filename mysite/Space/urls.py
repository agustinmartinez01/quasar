from django.conf.urls import url
from Space import views


space_detail = views.SpaceViewSet.as_view({
    'get': 'retrieve',
    # 'delete': 'destroy',
    # 'put': 'update',
    # 'patch': 'partial_update',
})
space_list = views.SpaceViewSet.as_view({
    'post': 'create',
    'get': 'list',
    
})

urlpatterns = [
    url(r'^satelite/$', space_list, name='space_list'),
    url(r'^satelite/(?P<slug>[-\w\d]+)', space_detail, name='space_detail'),
]