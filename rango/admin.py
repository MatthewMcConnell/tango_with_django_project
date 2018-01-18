from django.contrib import admin
from rango.models import Category, Page

class PageAdmin (admin.ModelAdmin):
    list_display = ("title", "category", "url")

<<<<<<< HEAD
class CategoryAdmin (admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Category, CategoryAdmin)
=======
admin.site.register(Category)
>>>>>>> eaa5e06... Added a page admin class to change the look of the admin page about pages to look like a table, also ran the population script
admin.site.register(Page, PageAdmin)
