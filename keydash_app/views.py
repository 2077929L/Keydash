from django.shortcuts import render

from django.http import HttpResponse

def about(request):
    return HttpResponse("Keydash about page! <br/> <a href='/keydash'>Index</a>")

def index(request):

    context_dict = {'boldmessage': "I am bold font from the context"}

    return render(request, 'keydash_app/index.html', context_dict)