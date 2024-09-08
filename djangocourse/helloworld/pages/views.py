from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.views import View
from django import forms
from .models import Product

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


class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.objects.all()
        return render(request, self.template_name, viewData)

class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            if product_id < 1:
                raise ValueError("Product ID must be greater 1 or greater")
            product = get_object_or_404(Product, id=product_id)
        except ValueError as e:
            return HttpResponseRedirect(reverse('home'))
        viewData = {}
        product = get_object_or_404(Product, id=product_id)
        viewData["title"] = product.name + " - Online Store"
        viewData["subtitle"] = product.name + " Product information"
        viewData["product"] = product 
        return render(request, self.template_name, viewData)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Price must be greater than zero.')
        return price

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
            form.save()
            
            # Redirect to a success page or another view
            return redirect('product-created')  # Replace with the actual URL name or path
        else:
            viewData = {
                "title": "Create Product",
                "form": form
            }
            return render(request, self.template_name, viewData)

class ProductUpdateView(View):
    model = Product
    template_name = 'products_list.html' 
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Products - Online Store'
        context['subtitle'] = 'List of products'
        return context  

class CartView(View):
    template_name = 'cart/index.html'

    def get(self, request):
        products = {}
        products[121] = {"name": "Tv Samsung", "price": 1000}
        products[11] = {"name": "Iphone", "price": 2000}

        cart_products = {}
        cart_product_data = request.session.get('cart_product_data', {})    

        for key, product in products.items():
            if str(key) in cart_product_data.keys():
                cart_products[key] = product

        view_data = {
            "title": "Cart - Online Store",
            "subtitle": "Shopping cart",
            "cart_products": cart_products
        }

        return render(request, self.template_name, view_data)
    

    def post(self, request, product_id):
        cart_product_data = request.session.get('cart_product_data', {})
        cart_product_data[product_id] = product_id
        request.session['cart_product_data'] = cart_product_data

        return redirect('cart_index')
    
class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_product_data' in request.session:
            del request.session['cart_product_data']

        return redirect('cart_index')

