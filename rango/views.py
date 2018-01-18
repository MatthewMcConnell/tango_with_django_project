from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

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
