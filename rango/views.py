from django.shortcuts import render 
from rango.models import Category
from django.http import HttpResponse 
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


def index(request):
  # Query the top 5 categories by likes
  category_list = Category.objects.order_by('-likes')[:5]

  # Query the top 5 pages by views
  page_list = Page.objects.order_by('-views')[:5]

  # Create a context dictionary to pass to the template
  context_dict = {
      'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
      'categories': category_list,
      'pages': page_list,
  }

  
  # Return a rendered response to send to the client.
  # We make use of the shortcut function to make our lives easier. 
  # Note that the first parameter is the template we wish to use. 
  return render(request, 'rango/index.html', context=context_dict)

def about(request):
  return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
  # Create a context dictionary which we can pass
  #  # to the template rendering engine. 
  context_dict = {}
  try:
    # Can we find a category name slug with the given name?
    # If we can't, the .get() method raises a DoesNotExist exception.
    # The .get() method returns one model instance or raises an exception. 
    category = Category.objects.get(slug=category_name_slug)
    # Retrieve all of the associated pages.
    # The filter() will return a list of page objects or an empty list. 
    # In views.py show_category()
    pages = category.page_set.all().order_by('title') 
    # Adds our results list to the template context under name pages.
    context_dict['pages'] = pages
    # We also add the category object from
    # the database to the context dictionary.
    # We'll use this in the template to verify that the category exists. 
    context_dict['category'] = category
  except Category.DoesNotExist:
    # We get here if we didn't find the specified category.
    # Don't do anything -
    # the template will display the "no category" message for us. 
    context_dict['category'] = None
    context_dict['pages'] = None
  # Go render the response and return it to the client.
  return render(request, 'rango/category.html', context=context_dict)
def add_category(request): 
  form = CategoryForm()
  if request.method == 'POST':
    form = CategoryForm(request.POST)
    if form.is_valid():
      form.save(commit=True)
      return redirect('/rango/')
    else:
      print(form.errors)
  return render(request, 'rango/add_category.html', {'form': form})

