from django.shortcuts import render
from django.contrib import messages
from .models import LocationDetail
from .forms import AddForm, SearchBox
import requests

def index(request):
    return render(request, 'index.html')

def add_location(request):
    message = ""
    result_list = []
    if request.method == 'GET':
            location = request.GET.get('name')
            if location != None:
                url = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q={}'

                try:
                    r = requests.get(url.format(location)).json()
                    for result in r:
                        result_detail = {
                            'name': result['nameEN'],
                            'address': result['addressEN'],
                            'xCoord': result['x'],
                            'yCoord': result['y'],
                        }
                        result_list.append(result_detail)
                except Exception as e:
                    message = "Fail to retrieve data from GeoDataStore!"

    else:
        new_name = request.POST.get('name')
        new_address = request.POST.get('address')
        new_xCoord = request.POST.get('xCoord')
        new_yCoord = request.POST.get('yCoord')
        new_location = LocationDetail(name=new_name, address=new_address, xCoord=new_xCoord, yCoord=new_yCoord)
        new_location.save()
        message = "New location added!"
        
    add_form = AddForm()

    context = {'result_list': result_list, 'add_form': add_form, 'message': message}

    return render(request, 'add_location.html', context)

def list_location(request):
    query = request.GET.get('name')
    reset = request.GET.get('reset')
    if query == None or reset == 'T':
        location_detail_list = LocationDetail.objects.all()
    else:
        location_detail_list = LocationDetail.objects.filter(name__icontains=query)
    
    search_box = SearchBox()
    context = {'location_detail_list': location_detail_list, 'search_box': search_box}

    return render(request, 'list_location.html', context)