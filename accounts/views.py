from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

from adverts.models import Category
from main.forms import MyRegistrationForm
from .forms import profileForm
from .models import Profile, PersonalMessage


# renders login page
def login(request):
    context = {}
    return render(request, 'registration/login.html')


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/accounts/invalid')


def invalid_login(request):
    return render(request, 'registration/invalid_login.html')


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/accounts/register_success')
    args = {}
    args['form'] = MyRegistrationForm()
    return render(request, 'registration/register.html', args)


def register_success(request):
    return render(request, 'registration/register_success.html')


@login_required
def view_profile(request):
    c = {}
    if Profile.objects.filter(user=request.user).exists():
        c['profile'] = Profile.objects.get(user=request.user)
        return render(request, 'view_profile.html', c)
    else:
        return HttpResponseRedirect('/accounts/create_profile/')


def public_profile(request, user_id):
    content = {}
    content['categories'] = Category.objects.all()

    content['user_id'] = user_id
    if Profile.objects.filter(user=user_id).exists():
        content['profile'] = Profile.objects.get(user=user_id)
    return render(request, 'public_profile.html', content)


@login_required()
def create_profile(request):
    if request.POST:
        form = profileForm(request.POST)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = request.user
            prof.save()
            return HttpResponseRedirect('/accounts/view_profile/')
    else:
        form = profileForm()
    return render(request, 'create_profile.html', {'form': form})


# edit profile page, allows user to make edits to their profile
@login_required()
def edit_profile(request):
    content = {}
    content['categories'] = Category.objects.all()
    if Profile.objects.filter(user=request.user).exists():
        profModel = Profile.objects.get(user=request.user)
        content['proform'] = profileForm(instance=profModel)
    else:
        return HttpResponseRedirect('/accounts/create_profile/')
    if request.POST:
        content['proform'] = proform = profileForm(request.POST, instance=profModel)
        if proform.is_valid():
            prof = proform.save(False)
            prof.user = request.user
            prof.save()
            return HttpResponseRedirect('/accounts/view_profile/')

    return render(request, 'edit_profile.html', content)


# function that handles sending personal messages to users, receives a
# POST request from the message box on the public profile page
# no related template
@login_required()
def send_message(request):
    # context dict to be passed to template
    c = {}
    # if request is POST, or, message form is submitted
    if request.POST:
        # set the recipient to the recipient user in the POST data
        recipient = User.objects.get(pk=request.POST['recipient'])
        # create personal message instance
        pm = PersonalMessage(
            # sender is the user who submitted the form
            sender=request.user,
            recipient=recipient,
            # message body in the POST data
            text=request.POST['text']
        )
        # save the message
        pm.save()
    # redirect to recipients public profile page
    return HttpResponseRedirect('/accounts/public_profile/%s/' % request.POST['recipient'])


# users inbox page, containing their received pms
@login_required()
def inbox(request):
    content = {}
    content['categories'] = Category.objects.all()
    # get the users received personal messages, order by sent_date
    content['messages'] = PersonalMessage.objects.filter(recipient=request.user.pk).order_by('-sent_date')
    # render inbox template and pass in messages
    return render(request, 'inbox.html', content)


# users outbox page, containing their sent pms
@login_required()
def outbox(request):
    content = {}
    content['categories'] = Category.objects.all()

    # get the users sent personal messages, order by sent_date
    content['messages'] = PersonalMessage.objects.filter(sender=request.user.pk).order_by('-sent_date')
    # render outbox template and pass in messages
    return render(request, 'outbox.html', content)

