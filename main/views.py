from django.shortcuts import render
from adverts.models import Category


# index view, home page
def index(request):
    # get all categories and add to dict
    content = dict()
    content['categories'] = Category.objects.all()
    # render index template and pass in context dict (categories)
    return render(request, 'index.html', content)


# currently not used
def error404(request):
    return render(request, '404.html')