from django.shortcuts import render, redirect
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

    # Return a rendered response to send to the client
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    # Create a context dictionary to pass to the template
    context_dict = {}

    try:
        # Find the category with the given slug
        category = Category.objects.get(slug=category_name_slug)
        # Retrieve all associated pages, ordered by title
        pages = category.page_set.all().order_by('title')
        # Add the pages and category to the context
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        # If the category doesn't exist, set context to None
        context_dict['category'] = None
        context_dict['pages'] = None

    # Render the response
    return render(request, 'rango/category.html', context=context_dict)

def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            # Redirect to the index page using reverse()
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        # Find the category with the given slug
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        # If the category doesn't exist, redirect to the index page
        return redirect(reverse('rango:index'))

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                # Save the page with the associated category
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                # Redirect to the category page using reverse()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    # Add the form and category to the context
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)