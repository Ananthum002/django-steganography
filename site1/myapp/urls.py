from django.urls import path
from django.urls import re_path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.index, name='index'),
    path('share', views.share, name='share'),
    path('recieved', views.recieved, name='recieved'),
    path('encode', views.encode, name='encode'),
    path('process_encoding_data', views.process_encoding_data, name='process_encoding_data'),
    path('decode', views.decode, name='decode'),
    path('decode_image_url', views.decode_image_url, name='decode_image_url'),
    path('process_decoding_data', views.process_decoding_data, name='process_decoding_data'),
    # re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
]