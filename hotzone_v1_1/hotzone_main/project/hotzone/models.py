from django.db import models

class VirusDetail(models.Model):
    name = models.CharField(max_length=100)
    commonName = models.CharField(max_length=100)
    maxInfectionPeriod = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class PatientDetail(models.Model):
    name = models.CharField(max_length=100)
    idNumber = models.CharField(max_length=10)
    dataOfBirth = models.DateField()

    def __str__(self):
        return f'{self.name} ({self.idNumber})'

class CaseDetail(models.Model):
    caseType_choices = [
        ("Local", "Local"),
        ("Import", "Import")
    ]
    caseNumber = models.CharField(max_length=5)
    virus = models.ForeignKey(VirusDetail, on_delete=models.CASCADE)
    patient = models.ForeignKey(PatientDetail, on_delete=models.CASCADE)
    date = models.DateField()
    caseType = models.CharField(max_length=10, choices=caseType_choices)

    def __str__(self):
        return self.caseNumber

class VisitedLocationDetail(models.Model):
    category_choices = [
        ("Residence", "Residence"),
        ("Workplace", "Workplace"),
        ("Visit", "Visit")
    ]
    caseNumber = models.ForeignKey(CaseDetail, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    dateFrom = models.DateField()
    dateTo = models.DateField()
    category = models.CharField(max_length=10, choices=category_choices)

    def __str__(self):
        return f'{self.caseNumber}: {self.name}'

class LocationDetail(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    xCoord = models.DecimalField(max_digits=8, decimal_places=2)
    yCoord = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name