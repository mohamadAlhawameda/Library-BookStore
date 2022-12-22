from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required
from .forms import BookForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

def book(request, pk):
    book = Book.objects.get(id=pk)
    context = {
        "page_title": "Books",
        "book": book,
    }

    return render(request, "bookdetail.html", context)

def books(request):
    books = Book.objects.all()
    context = {
        "page_title": "Books",
        "books": books,
    }
    return render(request, "home.html", context)

@login_required(login_url="login")
def addBook(request):
    form = BookForm()
    if request.method == 'POST':
        Book.objects.create(
            posted_by=request.user,
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            year=request.POST.get('year'),
            rating=request.POST.get('rating'),
            description=request.POST.get('description')
        )
        return redirect('/')

    context = {
        'form': form
    }
    return render(request, 'book_form.html', context)
@login_required(login_url="login")
def updateBook(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)

    if request.user != book.posted_by:
        return render(request, "not_authorized.html")

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.year = request.POST.get('year')
        book.rating = request.POST.get('rating')
        book.description = request.POST.get('description')
        book.save()
        return redirect('/')

    context = {'form': form, 'book': book}
    return render(request, 'book_form.html', context)
@login_required(login_url="login")
def deleteBook(request, pk):
    book = Book.objects.get(id=pk)

   
    if request.user != book.posted_by:
        return render(request, "not_authorized.html")

    if request.method == 'POST':
        book.delete()
        return redirect('/')
    return render(request, 'delete.html', {'obj': book})

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            print("Error")

    return render(request, 'login_register.html', {'form': form})

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            print('Doesnt exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Invalid username or passwors')

    context = {'page': page}
    return render(request, 'login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/')
