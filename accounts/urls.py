from django.conf.urls import url

from .views import *

app_name = 'accounts'

urlpatterns = (

    url(r'^login/$', login, name='login'),
    url(r'^auth/$', auth_view),
    url(r'^logout/$', logout, name='logout'),
    url(r'^invalid/$', invalid_login),
    url(r'^register/$', register_user, name='register'),
    url(r'^register_success/$', register_success),
    url(r'^view_profile/$', view_profile, name='view_profile'),
    url(r'^public_profile/(?P<user_id>\d+)/$', public_profile, name='public_profile'),
    url(r'^create_profile/$', create_profile, name='create_profile'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^send_message/$', send_message, name='send_message'),
    url(r'^inbox/$', inbox, name='inbox'),
    url(r'^outbox/$', outbox, name='outbox'),
)
