from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html, urlencode
from . import models
# Register your models here.

#custom filter
# class CustomerFilter(admin.SimpleListFilter):
#     title = 'membership'
#     parameter_name: str = 'membership'

#     def lookups(self, request, model_admin):
#         return [
#             ('BR', 'Bronze')
#         ]

#     def queryset(self, request, queryset):
#         if(self.value == 'BR'):
#             queryset.filter(membership)

@admin.register(models.Product) 
class ProductAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['']
    prepopulated_fields = {
        'slug':['title']
    }
    list_display= ['title', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product): 
        if product.inventory < 10:
            return "low"
        return 'OK'

@admin.register(models.Customer) 
class CustomerAdmin(admin.ModelAdmin):
    # actions = ['clear_list']     #custom action
    # autocomplete_fields = ['']
    # prepopulated_fields = {
    #     'slug':['first_name', 'last_name']
    # }    
    list_display= ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10  
    list_filter = ['membership']
    # ordering = ['first_name', 'last_name__startswith'] # join not permitted
     
    search_fields = ['first_name', 'last_name']


    # @admin.display(ordering='last _name')
    # def customer_count(self):
        # url = reverse('some-link') + '?' + urlencode({}) )
            # format_html('<a href=> {}</a>', )
    #     return models.Customer.

    # custom action
    # @admin.action(description='Clear List')
    # def clear_list(self, request, queryset):
    #     #some code
    #     pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']

admin.site.register(models.Collection) 


