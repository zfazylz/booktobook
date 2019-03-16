from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import AdvertForm
from .models import Advert, Comment, Category


def list_adverts(request, cat_id):
    content = dict()
    cat_id = int(cat_id)
    content['categories'] = Category.objects.all().order_by('id')

    if cat_id == 0:
        ads = Advert.objects.all().order_by('-pub_date')
    else:
        ads = Advert.objects.filter(category=cat_id).order_by('-pub_date')

    paginator = Paginator(ads, 5, allow_empty_first_page=True)

    page = request.GET.get('page')

    try:
        content['ads'] = paginator.page(page)
    except PageNotAnInteger:
        content['ads'] = paginator.page(1)
    except EmptyPage:
        content['ads'] = paginator.page(paginator.num_pages)

    return render(request, 'list_adverts.html', content)


@login_required()
def create_advert(request):
    if request.POST:
        # create a AdvertForm obj using the POSTed data
        form = AdvertForm(request.POST, request.FILES)
        # if the form validates
        if form.is_valid():
            # add the user to the form data before committing the save
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            # redirect to the list page, all categories
            return HttpResponseRedirect('/adverts/list_adverts/1')
    # else (not POST) create blank form obj
    else:
        form = AdvertForm()
    # render create template and pass in form obj
    return render(request, 'create_advert.html', {'form': form})


# display view, for displaying a single adverts details
def display_advert(request, advert_id):
    # context dict to be passed to template
    content = dict()
    content['categories'] = Category.objects.all().order_by('id')

    # get advert (or 404) using the advert_id argument
    content['ad'] = get_object_or_404(Advert, pk=advert_id)
    # render the template and pass in the advert
    return render(request, 'display_advert.html', content)


# edit advert view, for editing users adverts, login required
@login_required()
def edit_advert(request, advert_id):
    # context dict to be passed to template
    content = dict()
    content['category'] = Category.objects.all().order_by('id')

    # add advert_id to dict to be passed to template
    content['ad_id'] = advert_id
    # if the advert with the advert_id exits then
    if Advert.objects.filter(pk=advert_id).exists():
        # get that advert, set to variable
        ad = Advert.objects.get(pk=advert_id)
        # add the image to the template dict
        content['image'] = ad.image
        # create an advert form based on the ad to be edited
        content['ad'] = AdvertForm(instance=ad)
    # else create a blank advert form
    else:
        content['ad'] = AdvertForm()

    # if the request is POST, form being saved
    if request.POST:
        # create advert from with POSTed data
        adform = AdvertForm(request.POST, instance=ad)
        # if the form validates
        if adform.is_valid():
            # add the user to the form data before committing the save
            ad = adform.save(False)
            ad.user = request.user
            # forces an update instead of an insert (probably not needed, just being safe)
            ad.save(force_update=True)
            # redirect to display advert page, pass advert_id so correct ad is displayed
            return HttpResponseRedirect('/adverts/display_advert/%s' % (advert_id))
    # else render the edit template and pass in the advert to be edited
    else:
        return render(request, 'edit_advert.html', content)


# delete advert, no related template, just a function that takes
# in an advert_id and deletes it, login required
@login_required()
def delete_advert(request, advert_id):
    # if the advert exists then
    if Advert.objects.filter(pk=advert_id).exists():
        # get the adverts and
        ad = Advert.objects.get(pk=advert_id)
        # if the request user is the advert user then
        if request.user == ad.user:
            # delete the ad, doing this prevents someone from
            # deleting other users adverts through the URL
            ad.delete()
    # redirect to list adverts, all categories
    return HttpResponseRedirect('/adverts/list_adverts/0/')


# view all of a users adverts, takes in users id and gets
# adverts related to that user
def view_user_adverts(request, user_id):
    # context dict to be passed to template
    content = {}
    content['categories'] = Category.objects.all().order_by('id')

    # if there are adverts related to that user id then
    if Advert.objects.filter(user=user_id).exists():
        # get those adverts
        ads = Advert.objects.filter(user=user_id)
        # create the paginator
        paginator = Paginator(ads, 5, allow_empty_first_page=True)
        # GET the requested page
        page = request.GET.get('page')
        # try paginate based on requested page
        # return first page if page number is not an int
        # only show the last page if page is empty
        try:
            content['ads'] = paginator.page(page)
        except PageNotAnInteger:
            content['ads'] = paginator.page(1)
        except EmptyPage:
            content['ads'] = paginator.page(paginator.num_pages)
    # render user adverts template and pass in the users adverts
    return render(request, 'user_adverts.html', content)


# function for saving comment, no related template, receives POST
# from comment form on display advert page
@login_required()
def save_comment(request):
    # if request is POST, or, comment was posted
    if request.POST:
        # get the advert id from the hidden input 'ad_id'
        ad_id = request.POST['ad_id']
        # get the related advert instance
        ad = Advert.objects.get(pk=ad_id)
        # create a new comment instance
        com = Comment(
            user=request.user,
            advert=ad,
            text=request.POST['text'],
        )
        # save comment
        com.save()
    # redirect to same page as commenting from, display advert
    return HttpResponseRedirect('/adverts/display_advert/%s' % (request.POST['ad_id']))


# search function that renders the list adverts page with adverts based on
# search query received by a POST request from a search form on the base html page
def search(request):
    # context dict to be passed to template
    content = dict()
    content['categories'] = Category.objects.all().order_by('id')

    # if query is POSTed
    if request.POST:
        # assign category id from POST array
        # category id is taken from select box choice
        category = int(request.POST['category'])
        # assign query string from POST array
        query = request.POST['query']
        # if category id is 0 then query adverts of all categories
        # else query adverts with category id
        # title__icontians causes the query to return items where the title contains
        # the query string, case insensitive
        if category == 0:
            ads = Advert.objects.filter(title__icontains=query).order_by('-pub_date')
        else:
            ads = Advert.objects.filter(title__icontains=query, category=category)
        # create paginator
        paginator = Paginator(ads, 5, allow_empty_first_page=True)
        # GET requested page
        page = request.GET.get('page')
        # try paginate based on requested page
        # return first page if page number is not an int
        # only show the last page if page is empty
        try:
            content['ads'] = paginator.page(page)
        except PageNotAnInteger:
            content['ads'] = paginator.page(1)
        except EmptyPage:
            content['ads'] = paginator.page(paginator.num_pages)
        # if the context dict has no ads then create a new
        # key to contain a 'no results' message to be displayed
        # in the template
        if len(content['ads']) == 0:
            content['no_results'] = 'No search results found'
        # render the list adverts template and pass in the adverts
        # found relating to the search query
        return render(request, 'list_adverts.html', content)
