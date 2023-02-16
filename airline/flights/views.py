from django.shortcuts import render
from django.http import HttpResponse

def flights(request):
    return HttpResponse('Hello World!')
