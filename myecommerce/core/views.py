from django.contrib.auth import login
from django.shortcuts import render, redirect

# Create your views here.

# deplay  all data from the table product
from django.db.models import Q
from .forms import SignUpForm
from product.models import Product, Category

def frontpage(request):
    products = Product.objects.all()[0:8]

    return render(request, 'core/frontpage.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'core/signup.html', {'form': form})

def login_old(request):
    return render(request, 'core/login.html')

def shop(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    active_category = request.GET.get('category', '')

    if active_category:
        products = products.filter(category__slug=active_category)

    query = request.GET.get('query', '')
    

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    context = {
        'categories': categories,
        'products': products,
        'active_category': active_category
       
    }
    return render(request, 'core/shop.html', context)


