from django.shortcuts import render
from django.contrib import messages
from .models import LocationDetail, CaseDetail, VirusDetail, VisitedLocationDetail
from .forms import AddForm, SearchBox
import requests

def list_locations(request):
    locations_list = LocationDetail.objects.all()
    context = {'locations_list': locations_list}

    return render(request, 'list_locations.html', context)

def list_cases(request):
    cases_list = CaseDetail.objects.all()
    context = {'cases_list': cases_list}

    return render(request, 'list_cases.html', context)

def list_viruses(request):
    viruses_list = VirusDetail.objects.all()
    context = {'viruses_list': viruses_list}

    return render(request, 'list_viruses.html', context)

def show_location_detail(request, target):
    location = LocationDetail.objects.get(name = target)
    context = {'location': location}

    return render(request, 'show_location_detail.html', context)

def show_case_detail(request, target):
    case = CaseDetail.objects.get(caseNumber = target)
    patient = case.patient
    visited_locations_list = VisitedLocationDetail.objects.filter(caseNumber=case)
    context = {'case': case, 'patient': patient, 'visited_locations_list': visited_locations_list}

    return render(request, 'show_case_detail.html', context)

def show_virus_detail(request, target):
    virus = VirusDetail.objects.get(name = target)
    context = {'virus': virus}

    return render(request, 'show_virus_detail.html', context)

def add_visted_location(request, target):
    case = CaseDetail.objects.get(caseNumber = target)

    message = ""
    hotzone_results_list = []
    api_results_list = []
    if request.method == 'POST':
        if "search" in request.POST:
            location = request.POST.get("name")
            caseNumber = request.POST.get("caseNumber")
            dateFrom = request.POST.get("dateFrom")
            dateTo = request.POST.get("dateTo")
            category = request.POST.get("category")

            try:
                url = 'https://geodata.gov.hk/gs/api/v1.0.0/locationSearch?q={}'
                r = requests.get(url.format(location)).json()
                for result in r:
                    api_result_detail = {
                        'name': result['nameEN'],
                        'address': result['addressEN'],
                        'xCoord': result['x'],
                        'yCoord': result['y'],
                        'caseNumber': caseNumber,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo,
                        'category': category,
                    }
                    api_results_list.append(api_result_detail)
            except:
                code = requests.get(url.format(location)).status_code
                if (code == 400):
                    message = "Bad Request! Your input is invalid."
                elif (code == 500):
                    message = "Internal server error! Please try again later."
                else:
                    message = "Fail to retrieve data from GeoDataStore for unknown reasons!"
            
            try:
                records = LocationDetail.objects.filter(name__icontains=location)
                for record in records:
                    hotzone_result_detail = {
                        'name': record.name,
                        'address': record.address,
                        'xCoord': record.xCoord,
                        'yCoord': record.yCoord,
                        'caseNumber': caseNumber,
                        'dateFrom': dateFrom,
                        'dateTo': dateTo,                            
                        'category': category,
                    }
                    hotzone_results_list.append(hotzone_result_detail)
            except:
                print()
            message = "Result:"
        elif "add_new_location" in request.POST:
            location = request.POST.get("name")
            address = request.POST.get('address')
            xCoord = request.POST.get('xCoord')
            yCoord = request.POST.get('yCoord')
            caseNumber = request.POST.get("caseNumber")
            dateFrom = request.POST.get("dateFrom")
            dateTo = request.POST.get("dateTo")
            category = request.POST.get("category")
            case = CaseDetail.objects.get(caseNumber = caseNumber)
            new_visited_location = VisitedLocationDetail(caseNumber=case, name=location, dateFrom=dateFrom, dateTo=dateTo, category=category)
            new_location_record = LocationDetail(name=location, address=address, xCoord=xCoord, yCoord=yCoord)
            new_visited_location.save()
            new_location_record.save()
            message = "New visited location and location record added!"
        
        elif "add_visited_location" in request.POST:
            location = request.POST.get("name")
            caseNumber = request.POST.get("caseNumber")
            dateFrom = request.POST.get("dateFrom")
            dateTo = request.POST.get("dateTo")
            category = request.POST.get("category")
            new_visited_location = VisitedLocationDetail(caseNumber=case, name=location, dateFrom=dateFrom, dateTo=dateTo, category=category)
            new_visited_location.save()
            message = "New visited location added!"

    add_form = AddForm()
    context = {'case': case, 'add_form': add_form, 'hotzone_results_list': hotzone_results_list, 'api_results_list': api_results_list, 'message': message}

    return render(request, 'add_visited_location.html', context)
