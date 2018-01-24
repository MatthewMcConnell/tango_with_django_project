from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

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


@login_required
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


@login_required
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


def register (request):
    # boolean for telling the template whether registration
    # was successful
    registered = False

    # If it is a POST then we would like to process the form data
    if request.method == "POST":
        # Attempt to get the info
        user_form = UserForm (data = request.POST)
        profile_form = UserProfileForm (data = request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we hash the password, the we can update the user object
            user.set_password (user.password)
            user.save()

            # Now sorting the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems
            profile = profile_form.save (commit = False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so then add it
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            # Now saving the UserProfile model instance
            profile.save()

            # Updating the bool to indicate successful reg.
            registered = True
        else:
            # Print form problems to terminal
            print (user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using the
        # model form instances (these will be blank for user input)
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render (request,
                   "rango/register.html",
                   {"user_form": user_form,
                    "profile_form": profile_form,
                    "registered": registered})  


def user_login (request):
    # if request is POST then try to get the info
    if request.method == "POST":
        # using post.get instead as it is safer and nicer for
        # uses of the variables later on
        username = request.POST.get ("username")
        password = request.POST.get ("password")

        # using django's authentiction to see if they are valid
        user = authenticate (username = username, password = password)

        # check to see if user contains a user or not due to
        # successful/failed authentication
        if user:
            # Is the account active? It could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login (request, user)
                return HttpResponseRedirect (reverse("index"))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse ("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print ("Invalid login details: {0}, {1}".format (username, password))
            return HttpResponse ("Either you have not registered or you entered your username of password incorrectly")
    
    # The request is not POST, so display the login form
    else:
        # No context variables to pass to the template system
        return render (request, "rango/login.html", {})


@login_required
def restricted (request):
    return render (request, "rango/restricted.html", {})


# Using the login_required() decorator
@login_required
def user_logout (request):
    # Sinc we know the user is logge in, we can just log them out
    logout (request)
    # Take the user back to the homepage
    return HttpResponseRedirect (reverse ("index"))


