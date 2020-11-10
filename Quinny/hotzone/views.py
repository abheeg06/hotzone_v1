from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *


# Create your views here.
def index(request):
    model = LocationVisited
    """View function for home page of site."""

    # Generate counts of some of the main objects
    num_patient = Patient.objects.all().count()
    num_case = Case.objects.all().count()

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    # num_authors = Author.objects.count()

    location_visited = LocationVisited.objects.all()

    context = {
        'location_visited': location_visited,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def ajax_method():
    return HttpResponse(200)


def new_record(request):
    model = LocationVisited
    """View function for home page of site."""

    # Generate counts of some of the main objects

    # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    # num_authors = Author.objects.count()
    if request.method == "POST":
        form = LocationVisitedForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            return redirect('index')
    else:
        form = LocationVisitedForm()
    context = {
        'form': form
        # 'location_visited': location_visited,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'new_record.html', context=context)
