from django.conf.urls import url
from image_data import views

urlpatterns = [
    url(r'^images/$', views.index, name='index'),
    url(r'^images/(?P<pk>[0-9]+)/$', views.image_raw, name='image-raw')
]
