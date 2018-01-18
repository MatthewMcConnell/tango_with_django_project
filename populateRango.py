import os
os.environ.setdefault ("DJANGO_SETTINGS_MODULE", "tango_with_django_project.settings")

from random import randint

import django
django.setup()
from rango.models import Category, Page

def populate ():
    # Creating lists of dictionaries containing pages
    # Then creating a dictionary of dictionaries for 
    # the categories

    python_pages = [
        {"title": "Official Python Tutorial",
         "url": "http://docs.python.org/2/tutorial/"},
        {"title": "How to Think like a Computer Scientist",
         "url": "http://www.greenteapress.com/thinkpython/"},
        {"title": "Learn Python in 10 Minutes",
         "url": "http://www.korokithakis.net/tutorials/python/"} ]

    django_pages = [
        {"title": "Official Django Tutorial",
         "url": "https://docs.djangoproject.com/en/1.9/intro/tutorial01/"},
        {"title": "Django Rocks",
         "url": "http://www.djangorocks.com/"},
        {"title": "How to Tango with Django",
         "url": "http://www.tangowithdjango.com/"} ]

    other_pages = [
        {"title":"Bottle",
         "url":"http://bottlepy.org/docs/dev/"},
        {"title":"Flask",
         "url":"http://flask.pocoo.org"} ]
         
    cats = {"Python": {"pages": python_pages},
          "Django": {"pages": django_pages},
          "Other Frameworks": {"pages": other_pages} }

    # Add categories and pages to the above

    for cat, cat_data in cats.items():
        c = add_cat (cat)
        for p in cat_data["pages"]:
            add_page (c, p["title"], p["url"])

    for c in Category.objects.all():
        for p in Page.objects.filter (category = c):
            print ("- {0} - {1}".format (str(c), str(p)))

def add_page (cat, title, url):
    p = Page.objects.get_or_create (category = cat, title = title)[0]
    p.url = url
    p.views = randint (1, 20)
    p.save()
    return p

def add_cat (name):
    attributeMultiplier = 1

    if name == "Python":
        attributeMultiplier = 4
    elif name == "Django":
        attributeMultiplier = 2
        
    c = Category.objects.get_or_create (name = name, views = 32 * attributeMultiplier, likes = 16 * attributeMultiplier)[0]
    c.save()
    return c


# Execution starts here
if __name__ == "__main__":
    print ("Starting Rango population script...")
    populate()
