from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Keydash beginning of the project! <br/> <a href='/keydash/about'>About</a>" )

def about(request):
    return HttpResponse("Keydash about page! <br/> <a href='/keydash'>Index</a>")