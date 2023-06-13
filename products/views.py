from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib.auth.decorators import login_required

from .models import Product, Category, BookReview
# removed Quality, QualityVariant from imports
from .forms import ProductForm, BookReviewForm

def all_books(request):
    """ A view to display all books, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('title')) 
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "Please enter search criteria")
                return redirect(reverse('books'))
            
            queries = Q(title__icontains=query) | Q(blurb__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/books.html', context)


def book_detail(request, product_id):
    """ A view to display individual book details """
    product = get_object_or_404(Product, pk=product_id)
    is_in_wishlist = False
    if product.users_wishlist.filter(id=request.user.id).exists():
        is_in_wishlist = True
    # discounted_price = Product.discounted_price
    
    context = {
        'product': product,
        'is_in_wishlist': is_in_wishlist,
        # 'discounted_price': discounted_price,
    }
    template = 'products/book-detail.html'
    
    return render(request, template, context)

@login_required
def add_book(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added book')
            return redirect(reverse('book_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. \
            Please ensure all information is correct')
    else:
        form = ProductForm()
    template = 'products/add_book.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_book(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Successfully updated book: "{product.title}"')
            return redirect(reverse('book_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please \
            ensure all information is correct.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing book: "{product.title}"')

    template = 'products/edit_book.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_book(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, f'Book: "{product.title}" has been successfully deleted.')
    return redirect(reverse('books'))


@login_required
def add_book_review(request, product_id):
    """ A view to add a book review """
    if request.method == 'POST':
        book_form = BookReviewForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()
            messages.success(request, f"Your review for '{product.title} has been successfully added'")
        else:
            messages.error(request, f"Sorry, your review couldn't be saved. Please check all form fields are valid")
        return render(request, template_name='products/book-detail.html')
    book_form = BookReviewForm()
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'book_form': book_form,
    }
    template = 'products/book-detail.html'
    return render(request, template, context)