from django.shortcuts import render,redirect
from .models import Patient
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from .forms import ClinicalDataForm,ClinicalData
# Create your views here.

class PatientListView(ListView):
    model=Patient

class PatientCreateView(CreateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstname','lastname','age')

class PatientUpdateView(UpdateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstname','lastname','age')

class PatientDeleteView(DeleteView):
    model=Patient
    success_url=reverse_lazy('index')

def addData(request,**kwargs):
    form=ClinicalDataForm()
    patient=Patient.objects.get(id=kwargs['pk'])
    if request.method=="POST":
        form=ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/")
    return render(request,'ClinicalApp/data_form.html',{'form':form,'patient':patient})
    

def analyze(request,**kwargs):
    data=ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData=[]
    for eachEntry in data:
        if eachEntry.componentname=="hw":
            heightAndWeight=eachEntry.componentvalue.split('/')
            if len(heightAndWeight)>1:
                feetToMetres=float(heightAndWeight[0])*0.4536
                BMI=(float(heightAndWeight[1]))/(feetToMetres*feetToMetres)
                bmiEntry=ClinicalData()
                bmiEntry.componentname='BMI'
                bmiEntry.componentvalue=BMI
                responseData.append(bmiEntry)
            responseData.append(eachEntry)
        return render(request,'ClinicalApp/generationReport.html',{'data':data})
