#file: quotes/views.py
import random
import time
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


quotes = [
    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "It always seems impossible, until it is done",
    "Lead from the back – and let others believe they are in front",
    ] 

images = [
    "https://res.cloudinary.com/aenetworks/image/upload/c_fill,ar_2,w_3840,h_1920,g_auto/dpr_auto/f_auto/q_auto:eco/v1/nelson-mandela-gettyimages-587487938?_a=BAVAZGID0",
    "https://www.businessandleadership.com/wp-content/uploads/2017/07/mandela-1024x551.jpg",
    "https://www.nobelprize.org/images/mandela-13452-portrait-medium.jpg",
]


# Create your views here.
def home(request):
    '''Fund to respond to the "home" page request'''

    response_test = '''
    <html>
    <h1>Hello World!</h1>
    <html>
    '''

    return HttpResponse(response_test)

def quote(request):
    template_name = 'quotes/quote.html'
    context = {
        "time": time.ctime(),
        "quote": random.choice(quotes),
        "quote_img": random.choice(images),
    }
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'
    context = {
        "time": time.ctime(),
        "quotes": quotes,
        "images": images,
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'quotes/about.html'
    context = {
        "time": time.ctime(),
    }
    return render(request, template_name, context)