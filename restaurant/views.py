from django.shortcuts import render
from django.http import HttpResponse
import time
import random
# Create your views here.

def main(request):
    '''Show the main page to the user.'''
    context = {"time": time.ctime()}
    template_name = 'restaurant/main.html'
    return render(request, template_name=template_name, context=context)

def order(request):
    '''Show the ordering page.'''
    template_name = 'restaurant/order.html'

    daily_special = [
        'Blueberry Chocolate Muffin',
        'Nutella & Strawberry Croissant', 
        'Pein en Double Chocolat', 
        'Raspberry Danish'
    ]
    random_index = random.randint(0, len(daily_special)-1)
    
    context = {"time": time.ctime(),
               "special": daily_special[random_index]
               }

    return render(request, template_name = template_name, context = context)

def submit_order(request):
    '''Process the  form submitted and generate result.'''

    template_name = 'restaurant/confirmation.html'
    # print(request)

    # check if the form was submitted
    if request.POST:

        # extract form fields into variables
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        item1 = request.POST.get('item1', "None")
        print("item1", item1)
        item2 = request.POST.get('item2', "None")
        item3 = request.POST.get('item3', "None")
        item4 = request.POST.get('item4', "None")
        item5 = request.POST.get('item5', "None")
        special_instructions = request.POST['special_instructions']

        total_price = 0.0

        def split(item):
            if item and '$' in item:
                parts = item.split('$')
                return parts[0], parts[1]
            return None, 0.0
    
        item1_name, price1 = split(item1)
        item2_name, price2 = split(item2)
        item3_name, price3 = split(item3)
        item4_name, price4 = split(item4)
        item5_name, price5 = split(item5)

        total = round(float(price1) + float(price2) + float(price3) + float(price4) + float(price5), 2)

        # create context variables 
        context = {
                'name': name, 
               'number': number,
               'time': time.ctime(),
               'email': email,
               'item1': item1_name,
               'item2': item2_name,
               'item3': item3_name,
               'item4': item4_name,
               'item5': item5_name,
               "price1": price1,
               "price2": price2,
               "price3": price3,
               "price4": price4,
               "price5": price5,
               'special_instructions': special_instructions,
               'total': float(total),
               'ready_time': time.ctime(time.time() + 40*60) 
               }
    return render(request, template_name=template_name, context=context)
    # return HttpResponse("")

