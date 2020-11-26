from .models import LocationDetail, CaseDetail, VirusDetail, VisitedLocationDetail
from .forms import AddForm, SearchBox, CustomUserCreationForm
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from sklearn.cluster import DBSCAN
from datetime import date
import math
import requests
import numpy as np

def custom_metric(q, p, space_eps, time_eps):
    dist = 0
    for i in range(2):
        dist += (q[i] - p[i])**2
    spatial_dist = math.sqrt(dist)

    time_dist = math.sqrt((q[2]-p[2])**2)

    if time_dist/time_eps <= 1 and spatial_dist/space_eps <= 1 and p[3] != q[3]:
        return 1
    else:
        return 2


def cluster(vector_4d, distance, time, minimum_cluster):

    params = {"space_eps": distance, "time_eps": time}
    db = DBSCAN(eps=1, min_samples=minimum_cluster-1, metric=custom_metric, metric_params=params).fit_predict(vector_4d)

    unique_labels = set(db)
    total_clusters = len(unique_labels) if -1 not in unique_labels else len(unique_labels) -1

    print("Total clusters:", total_clusters)

    total_noise = list(db).count(-1)

    print("Total un-clustered:", total_noise)

    clusters = []

    for k in unique_labels:
        if k != -1:

            labels_k = db == k
            cluster_k = vector_4d[labels_k]

            pts = []
            for pt in cluster_k:
                pts.append({'x': pt[0], 'y': pt[1], 'day': pt[2], 'caseNo': pt[3]})
            
            cluster = {'number': k+1, 'size': len(cluster_k), 'pts': pts}
            clusters.append(cluster)

    result = {'total_clusters': total_clusters, 'total_noise': total_noise, 'clusters': clusters}
    return result

def user_creation(request): 
    if request.user.is_authenticated:
        return redirect('list_cases')
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_login')
        else:
            form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'user_creation.html', context)

def user_login(request):
    if request.user.is_authenticated:
        return redirect('list_cases')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_cases')
    context = {}
    return render(request, 'user_login.html', context)

def user_logout(request):
    logout(request)
    return render(request, 'user_logout.html')

@login_required(login_url='user_login')
def list_locations(request):
    locations_list = LocationDetail.objects.all()
    context = {'locations_list': locations_list}

    return render(request, 'list_locations.html', context)

@login_required(login_url='user_login')
def list_cases(request):
    cases_list = CaseDetail.objects.all()
    context = {'cases_list': cases_list}

    return render(request, 'list_cases.html', context)

@login_required(login_url='user_login')
def list_viruses(request):
    viruses_list = VirusDetail.objects.all()
    context = {'viruses_list': viruses_list}

    return render(request, 'list_viruses.html', context)

@login_required(login_url='user_login')
def show_location_detail(request, target):
    location = LocationDetail.objects.get(name = target)
    context = {'location': location}

    return render(request, 'show_location_detail.html', context)

@login_required(login_url='user_login')
def show_case_detail(request, target):
    case = CaseDetail.objects.get(caseNumber = target)
    patient = case.patient
    visited_locations_list = VisitedLocationDetail.objects.filter(caseNumber=case)
    context = {'case': case, 'patient': patient, 'visited_locations_list': visited_locations_list}

    return render(request, 'show_case_detail.html', context)

@login_required(login_url='user_login')
def show_virus_detail(request, target):
    virus = VirusDetail.objects.get(name = target)
    context = {'virus': virus}

    return render(request, 'show_virus_detail.html', context)

@login_required(login_url='user_login')
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
            check_existing = LocationDetail.objects.filter(xCoord=xCoord, yCoord=yCoord)
            if not check_existing:
                new_location_record.save()
            new_visited_location.save()
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

@login_required(login_url='user_login')
def view_clusters(request):
    paras = {'D': 200, 'T': 3, 'C': 2}
    context = {'flag': -1, 'paras': paras}
    if "view" in request.POST:
        dots_list = []
        visitedLocations = VisitedLocationDetail.objects.all()
        for visitedLocation in visitedLocations:
            locationDetail = LocationDetail.objects.get(name=visitedLocation.name)
            d0 = date(2020, 1, 1)
            delta = visitedLocation.dateFrom - d0
            dots_list.append([locationDetail.xCoord, locationDetail.yCoord, delta.days, visitedLocation.caseNumber.caseNumber])
        dots_array = np.array(dots_list)
        D = int(request.POST.get("distance"))
        T = int(request.POST.get("time"))
        C = int(request.POST.get("size"))
        result = cluster(dots_array, D, T, C)
        paras = {'D': D, 'T': T, 'C': C}
        context = {'result': result, 'flag': 1, 'paras': paras}

    return render(request, 'view_clusters.html', context)
