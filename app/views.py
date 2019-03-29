from django.shortcuts import render, get_object_or_404
from .models import Person, Department, Product
from django.db.models import Q

# Create your views here.

def index_view(request):
    return render(request, 'app/index.html')

def contacts_search_view(request):
    departments = Department.objects.all()
    return render(request, 'app/contacts_search.html', {'departments': departments})

def contacts_view(request):
    contact_search = request.POST.get('contact_search')
    people = Person.objects.filter(Q(lname__contains=contact_search) | Q(fname__contains=contact_search)).order_by('lname')
    return render(request, 'app/contacts.html', {'people': people})

def department_contacts_view(request):
    dep = request.POST.get('department')
    people = Department.objects.get(pk=dep).get_people()
    return render(request, 'app/contacts.html', {'people': people})

def pv_view(request):
    return render(request, 'app/pv.html')

def psur_view(request):
    return render(request, 'app/psur.html')

def adrs_view(request):
    return render(request, 'app/adrs.html')

def ct_view(request):
    return render(request, 'app/ct.html')

def reg_view(request):
    return render(request, 'app/reg.html')

def products_view(request):
    products = Product.objects.all()
    return render(request, 'app/product.html', {'products': products})

def product_details_view(request, id):
    product = Product.objects.get(pk=id)
    return render(request, 'app/product.html', {'product': product})

