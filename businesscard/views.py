from django.shortcuts import render
from .models import *

def map(request):
    return render(request, "index.html")
def statistics(request):
    return render(request, "statistics.html")
def predict(request):
    return render(request, "predict.html")
def create_model(request):
    return render(request, "create_model.html")
def docs(request):
    return render(request, "docs.html")
def location(request):
    return render(request, 'location.html')