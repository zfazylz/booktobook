from django.urls import path
from .views import *


app_name = 'main'

urlpatterns = (

    path('', index, name='index'),

)

handler404 = 'classified.views.error404'
