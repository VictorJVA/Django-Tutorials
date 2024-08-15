from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views import View
from django import forms

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Victor",
        })
        return context

class AboutContactView(TemplateView):
    template_name = 'pages/contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "description": "This is a contact page ...",
            "email": "vic@gmail.com",
            "phone": "1234567890",
            "address": "123 Main St, New York, NY 10030",
        })
        return context

class Product:
    products = [
        {"id": "1", "name": "TV", "description": "Best TV", "price": 1000},
        {"id": "2", "name": "iPhone", "description": "Best iPhone", "price": 1100},
        {"id": "3", "name": "Chromecast", "description": "Best Chromecast", "price": 50},
        {"id": "4", "name": "Glasses", "description": "Best Glasses", "price": 100},
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        viewData = {}
        product = Product.products[int(id)-1]
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " Product information"
        viewData["product"] = product 
        return render(request, self.template_name, viewData)

class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

class ProductCreateView(View):
    template_name = 'products/create.html'

    def get(self, request):
        form = ProductForm()
        viewData = {
            "title": "Create Product",
            "form": form
        }
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Process the form data here
            # For example, save the data to the database
            # product = Product(name=form.cleaned_data['name'], price=form.cleaned_data['price'])
            # product.save()
            
            # Redirect to a success page or another view
            return redirect('product_list')  # Replace with the actual URL name or path
        else:
            viewData = {
                "title": "Create Product",
                "form": form
            }
            return render(request, self.template_name, viewData)    