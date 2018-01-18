from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index (request):
    # Querying the database and getting the top 5 liked categories to 
    # put into context_dict
    category_list = Category.objects.order_by ("-likes") [:5]
    context_dict = {"categories": category_list}

    # Querying again to get the top 5 viewed pages to put into
    # context_dict
    pageList = Page.objects.order_by ("-views") [:5]
    context_dict["pages"] = pageList

    # Return a rendered response to send to the client.
    return render (request, "rango/index.html", context=context_dict)

def about (request):
    return render (request, "rango/about.html")

def show_category (request, category_name_slug):
    # Creating a context dictionary to pass to render
    context_dict = {}

    try:
        # Tries to find a category name slug with the given name
        category = Category.objects.get (slug = category_name_slug)

        # Retrieve all of the associated pages
        pages = Page.objects.filter (category = category)

        # Adds the page results list to the template context
        context_dict["pages"] = pages

        # Also adding the category to context so it can verify the category exists
        context_dict["category"] = category

    except:
        # We execute this if we didn't find the category
        context_dict["category"] = None
        context_dict["pages"] = None

    return render (request, "rango/category.html", context_dict)


def add_category (request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == "POST":
        form = CategoryForm (request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database
            form.save (commit = True)
            # We could give a confimation message to say its
            # been added but instead we'll direct them back
            # to the index page as it'll be on there anyway
            return index (request)
        else:
            # Just print the form errors to the terminal
            print (form.errors)
    
    # Will handle the bad form, new form, or
    # no form supplied cases.
    # Render the form with error messages (if any)
    return render (request, "rango/add_category.html", {"form": form})


def add_page (request, category_name_slug):
    try:
        category = Category.objects.get (slug = category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    # A HTTP POST?
    if request.method == "POST":
        form = PageForm (request.POST)

        # Check if the form is valid
        if form.is_valid():
            if category:
                page = form.save (commit = False) # why is this false?
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print (form.errors)

    context_dict = {"form": form, "category": category}
    return render (request, "rango/add_page.html", context_dict)

