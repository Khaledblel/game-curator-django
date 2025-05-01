from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('recommender')
        messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserCreationForm()
    return render(request, 'authentication/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                # Redirect to the page they were trying to access or default to recommender
                next_page = request.GET.get('next', 'recommender')
                return redirect(next_page)
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('landing_page')

@login_required
def update_username(request):
    """Update the current user's username"""
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        
        if not new_username or len(new_username.strip()) == 0:
            return JsonResponse({'success': False, 'error': 'Username cannot be empty'})
            
        # Check if username is already taken
        from django.contrib.auth.models import User
        if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
            return JsonResponse({'success': False, 'error': 'This username is already taken'})
            
        try:
            # Update username
            user = request.user
            user.username = new_username
            user.save()
            
            return JsonResponse({'success': True, 'username': new_username})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    # If not POST method
    return JsonResponse({'success': False, 'error': 'Invalid request method'})