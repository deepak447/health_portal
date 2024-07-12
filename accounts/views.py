from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate, logout 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomSignupForm, BlogPostForm
from django.contrib.auth.decorators import login_required
from .models import BlogPost


def signup(request):
    """
    Handles user Signup requests.

    This view function allows users to create new accounts. 
    It processes POST data to create a new user and logs them in. 
    If the request is GET, it displays the blank signup form.
    """
    if request.method == 'POST':
         # Create CustomSignupForm  from POST data and uploaded files
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid(): # check form is valid 
            user = form.save() # save the data 
            login(request, user) # login new created user
            messages.success(request, 'Signup successful! Welcome.') 
            return redirect('/login')    # Redirect the user to the login page
        else:  # **Highlight: Return the form with errors if not valid**
            messages.warning(request, "Write correct password")
            return render(request, 'signup.html', {'form': form}) 
    else:
        form = CustomSignupForm() # Create an empty CustomSignupForm instance for the signup form
        return render(request, 'signup.html', {'form': form})
    


def user_login(request):
    """
    Handles user login requests.

    This view function processes login attempts. 
    It checks if the provided credentials are valid and logs the user in.
    It then redirects the user to their appropriate dashboard based on their user type.
    """
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)# Create an AuthenticationForm instance with POST data
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.user_type == 'patient':
                    return redirect('/patient_dashboard/')  
                elif user.user_type == 'doctor':
                    return redirect('/doctor_dashboard/')  
    else:
        form = AuthenticationForm()# Create an empty AuthenticationForm instance for login form
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    """
    Logout the current user .

    This view function handles user logout requests. It logout the current user 
    and redirects them to the login page.
    """
    logout(request)
    return redirect('/login')  


def patient_dashboard(request):
    """
    Renders the patient dashboard.

    This view function renders the patient_dashboard.html template, 
    passing the current user object to the template for access within the dashboard.
    """
    user = request.user  # Get the currently logged-in user
    context = {'user': user} # Create a context dictionary with the user object
    return render(request, 'patient_dashboard.html', context)

def doctor_dashboard(request):
    """
    Renders the doctor dashboard.

    This view function renders the doctor_dashboard.html template, 
    passing the current user object to the template for access within the dashboard.
    """
    if request.user.is_authenticated and request.user.user_type == 'doctor':
        blogs = BlogPost.objects.filter(author=request.user)
    user = request.user
    context = {'user': user,"blog": blogs}
    return render(request, 'doctor_dashboard.html', context)# render templates

@login_required
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
                # blog_post.draft = True
            blog_post.save()
            if blog_post.draft:
                messages.success(request, "Blog post saved as draft.")
            else:
                messages.success(request, "Blog post published.")
            return redirect('home')
    else:
        form = BlogPostForm()

    context = {
        'form': form,
    
    }
    return render(request, 'write_blog.html', context=context)

@login_required
def patient_blog(request):
    posts = BlogPost.objects.filter(draft=False).order_by('-id') # Fetch non-draft posts from DB

    if not posts:
        return redirect('patient_dashboard/')

    context = {
        'posts': posts,
    }
    return render(request, 'patient.html', context=context)

@login_required
def home(request):
    posts = BlogPost.objects.filter(draft=True, author=request.user).order_by('-id') # Fetch all posts from DB
    
    if not posts:
        return redirect('doctor_dashboard/')

    for post in posts:
        if len(post.summary.split()) > 15:
            post.summary = " ".join(post.summary.split()[:15]) + "..."
    # print(posts)
    context = {
        'posts': posts,
    }
    return render(request, 'home.html', context=context)