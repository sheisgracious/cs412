from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def show_form(request):
    '''Show the form to the user.'''

    template_name = 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    '''Process the  form submitted and generate result.'''

    template_name = 'formdata/confirmation.html'
    print(request)

    # check if the form was submitted
    if request.POST:

        # extract form fields into variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        # create conext variables 
        context = {'name': name, 
                   'favorite_color': favorite_color}
        
    return render(request, template_name=template_name, context=context)
    # return HttpResponse("")

