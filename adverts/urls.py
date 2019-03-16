from django.urls import path
from .views import *
from django.urls import path

from .views import *

app_name = 'adverts'

urlpatterns = (

    path('list_adverts/<cat_id>', list_adverts, name='list'),
    path('create_advert/', create_advert, name='create'),
    path('edit_advert/<advert_id>', edit_advert, name='edit'),
    path('delete_advert/<advert_id>', delete_advert, name='delete'),
    path('display_advert/<advert_id>', display_advert, name='display'),
    path('user_adverts/<user_id>', view_user_adverts, name='user_adverts'),
    path('search/', search, name='search'),
    path('save_comment/', save_comment, name='save_comment'),
)

handler404 = 'classified.views.error404'
