from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.template.defaultfilters import slugify

from .forms import CoffeeForm
from users.forms import UserProfileForm

from users.models import UserProfile
from .models import Coffee
from users import utils
from .utils import get_coffee

from cat.forms import CategoryForm, CoffeeItemForm
from cat.models import Category, CoffeeItem

from orders.models import Order, OrderedCoffee



@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    coffee = get_object_or_404(Coffee, user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        coffee_form = CoffeeForm(request.POST, request.FILES, instance=coffee)
        if profile_form.is_valid() and coffee_form.is_valid():
            profile_form.save()
            coffee_form.save()

            # Geocode the address and update the profile
            address = profile_form.cleaned_data.get('address')
            if address:
                geo = utils.geocode_address(address)
                if geo:
                    profile.latitude, profile.longitude = geo
                    profile.save()

            messages.success(request, 'Settings updated.')
            return redirect('cprofile')
        else:
            print(profile_form.errors)
            print(coffee_form.errors)
    else:
        profile_form = UserProfileForm(instance=profile)
        coffee_form = CoffeeForm(instance=coffee)

    context = {
        'profile_form': profile_form,
        'coffee_form': coffee_form,
        'profile': profile,
        'coffee': coffee,
    }
    return render(request, 'coffee/cprofile.html', context)


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def menus(request):
    coffee = get_coffee(request)
    categories = Category.objects.filter(coffee=coffee).order_by('created_at')
    context = {
        'categories': categories,
    }
    return render(request, 'coffee/menus.html', context)

def coffeeitems_by_category(request, pk=None):
    ...


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.coffee = get_coffee(request)
            
            category.save() # when the category object is saved the the category id will be generated
            category.slug = slugify(category_name)+'-'+str(category.id) #chicken-15 first is name second is category id
            category.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menus')
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    context = {
        'form': form,
    }
    return render(request, 'coffee/add_category.html', context)


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def edit_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category = form.save(commit=False)
            category.coffee = get_coffee(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menus')
        else:
            print(form.errors)
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request,'coffee/edit_category.html', context)


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def delete_category(request, pk=None):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully!')
    return redirect('menus')
    

@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def add_coffee(request):
    if request.method == 'POST':
        form = CoffeeItemForm(request.POST, request.FILES)
        if form.is_valid():
            coffeetitle = form.cleaned_data['coffee_name']
            coffee = form.save(commit=False)
            coffee.coffee = get_coffee(request)
            coffee.slug = slugify(coffeetitle)
            form.save()
            messages.success(request, 'Coffee Item added successfully!')
            return redirect('coffeeitems_by_category', coffee.category.id)
        else:
            print(form.errors)
    else:
        form = CoffeeItemForm()
        # only prints categories which belongs to logged in user
        form.fields['category'].queryset = Category.objects.filter(coffee=get_coffee(request))
    context = {
        'form': form,
    }
    return render(request, 'coffee/add_coffee.html', context)


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def edit_coffee(request, pk=None):
    coffee = get_object_or_404(CoffeeItem, pk=pk)
    if request.method == 'POST':
        form = CoffeeItemForm(request.POST, request.FILES, instance=coffee)
        if form.is_valid():
            coffeetitle = form.cleaned_data['coffee_name']
            coffee = form.save(commit=False)
            coffee.coffee = get_coffee(request)
            coffee.slug = slugify(coffeetitle)
            form.save()
            messages.success(request, 'Coffee Item updated successfully!')
            return redirect('coffeeitems_by_category', coffee.category.id)
        else:
            print(form.errors)
    else:
        form = CoffeeItemForm(instance=coffee)
        # to display categories which belongs to logged in user
        form.fields['category'].queryset = Category.objects.filter(coffee=get_coffee(request))
    context = {
        'form': form,
        'coffee': coffee,
    }
    return render(request,'coffee/edit_coffee.html', context)


@login_required(login_url='login')
@user_passes_test(utils.check_coffee_role)
def delete_coffee(request, pk=None):
    coffee = get_object_or_404(CoffeeItem, pk=pk)
    coffee.delete()
    messages.success(request, 'Coffee Item has been deleted successfully!')
    return redirect('coffeeitems_by_category', coffee.category.id)


def order_detail(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_coffee = OrderedCoffee.objects.filter(order=order, coffeeitem__coffee=get_coffee(request))
    
        context = {
            'order': order,
            'ordered_coffee': ordered_coffee,
            'subtotal': order.get_total_by_coffee()['subtotal'],
            'grand_total': order.get_total_by_coffee()['grand_total'],
        }  
    except:
        return redirect('coffee')
    return render(request, 'customers/order_detail.html', context)
