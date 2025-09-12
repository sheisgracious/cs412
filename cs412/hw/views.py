#file: hw/views.py
import random
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.
def home(request):
    '''Fund to respond to the "home" page request'''

    response_test = '''
    <html>
    <h1>Hello World!</h1>
    <html>
    '''

    return HttpResponse(response_test)

def home_page(request):
    template_name = 'hw/home.html'
    # dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(78, 90)),
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'hw/about.html'
    # dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(78, 90)),
    }
    return render(request, template_name, context)