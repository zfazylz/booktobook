from django.contrib import admin
from .models import Profile, PersonalMessage


class profileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name')


class PersonalMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'text', 'sent_date')


# register your models with the admin section
admin.site.register(Profile, profileAdmin)
admin.site.register(PersonalMessage, PersonalMessageAdmin)
