from django.db import models

# Create your models here.

class Patient(models.Model):

    name = models.CharField(max_length=50)
    id_num = models.CharField(max_length=10)
    date_of_birth = models.DateField()

class Virus(models.Model):
    name = models.CharField(max_length=50)
    common_name = models.CharField(max_length=50)
    max_infection_date = models.IntegerField()

class LocationVisited(models.Model):
    CATAGORYS = [
        ('R', 'Residence'),
        ('W', 'Workplace'),
        ('V', 'Visit')
    ]
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True)
    x = models.CharField(max_length=50)
    y = models.CharField(max_length=50)
    date_from = models.DateField()
    date_to = models.DateField()
    catagory = models.CharField(max_length=1, choices = CATAGORYS)

class Case(models.Model):
    SOURCES = [
        ('L', 'LOCAL'),
        ('I', 'IMPORTED'),
    ]
    location_visited = models.ForeignKey(LocationVisited, on_delete=models.PROTECT, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    infecting_virus = models.ForeignKey(Virus, on_delete=models.PROTECT)
    confirm_date = models.DateField()
    source = models.CharField(max_length=1, choices=SOURCES)
