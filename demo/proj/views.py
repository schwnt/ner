from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.http import JsonResponse
from . import apps

def app(request): 
    template = loader.get_template('home.html')
    return HttpResponse(template.render(apps.GetTemplateContext()))

def data(request):
    if 'u' in request.GET:
        url = request.GET['u']
        if 'm' in request.GET :
            model_name = request.GET['m']
            data = apps.GetData(url, model_name)
        else : 
            data = apps.GetData(url)
        return JsonResponse(data)
    else: return JsonResponse({})

