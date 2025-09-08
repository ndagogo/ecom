from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Banner
from .forms import ProductForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Q


def home(request):
    products = Product.objects.all()[:8]  # show trending/latest 8 products
    banners = Banner.objects.filter(is_active=True)
    return render(request, "shop/home.html", {"products": products, "banners": banners})


def product_list(request):
    query = request.GET.get("q")
    product_list = Product.objects.all()

    if query:
        product_list = product_list.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Pagination: 6 products per page (adjust as needed)
    paginator = Paginator(product_list, 6)
    page_number = request.GET.get("page")
    products = paginator.get_page(page_number)

    return render(
        request,
        "shop/product_list.html",
        {"products": products, "query": query},
    )



def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "shop/product_detail.html", {"product": product})

def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # request.FILES added
        if form.is_valid():
            form.save()
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "shop/add_product.html", {"form": form})

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)  # request.FILES added
        if form.is_valid():
            form.save()
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "shop/edit_product.html", {"form": form, "product": product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("product_list")
    return render(request, "shop/delete_product.html", {"product": product})
