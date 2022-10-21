import datetime
from django.http import HttpResponse,HttpResponseRedirect
from django.views import generic
from django.shortcuts import render,get_object_or_404
from django.views.generic import TemplateView
from django.utils import timezone
from .models import SerialNumbersManager,Logs, Reworks, Products, SerialNumbers, ProductsHasReworks, Models, Manufacturers, Batchs, Tests, TestBenchs
from .forms import productform

#vue avec le choix du produit



def ProductSearch(request):
    context = {}
    if request.GET.get('search',False):
        context = iniproduct(request,context)
    if request.GET.get('reworksearch',False):
        context = inirework(request,context)
    return render(request, 'reworking/index.html',context)

def inirework(request,context):
    search_term =request.GET.get('reworksearch',False)
    reworks = get_object_or_404(Reworks,designator__startswith=search_term)
    context['possible_reworks_list'] = reworks
    return context

def iniproduct(request,context):
    search_term = request.GET.get('search', False)
    idserial = search_term[0:search_term.find('-')]
    product = get_object_or_404(Products, serial_number_id=idserial)
    context = {'serial_number': SerialNumbers.objects.value(idserial),
               'model': product.model,
               'elec_result': product.electrical_result,
               'functional_result': product.functional_result,
               'reworks_list': ProductsHasReworks.objects.filter(product_id=product).order_by('date'),
               'reworks_list_total' : ProductsHasReworks.objects.all().values_list('rework__designator',flat = True),
               'possible_reworks_list': Tests.objects.reworks_test(Logs.objects.filter(product=product, result='nok').order_by('date')[0].test.id_test),
               'last_log_failed': Logs.objects.filter(product=product, result='nok').order_by('date')[0],
               #'proba_list': ProductsHasReworks.objects.probalist(Logs.objects.filter(product=product, result='nok').order_by('date')[0].test.id_test)
               }
    return context