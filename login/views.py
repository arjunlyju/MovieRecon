from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, update_session_auth_hash, authenticate,login
from django.urls import reverse
from.forms import UserForm

# Create your views here.

def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('Password')
        user=auth.authenticate(username=username,password=password)
        # if user is not None and not user.is_administrator:
        if user is not None and not user.is_staff:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credntials')
            return redirect('login:login')

    return render(request,'login.html')

def register(request):
    User = get_user_model()
    if request.method=='POST':
        username=request.POST.get('username')
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        email=request.POST.get('email')
        password=request.POST.get('psw')
        cpassword=request.POST.get('psw-repeat')
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('login:register')
            else:
                user=User.objects.create_user(username=username,password=password,first_name=fname,last_name=lname,email=email)
                user.save()
                # Authenticate the user
                user_authenticated  = authenticate(username=username, password=password)
                if user_authenticated is not None:
                    # Log the user in
                    request.session['new_registration'] = True  # Set session variable
                    login(request,user_authenticated )
                    return redirect("login:login")
                else:
                    messages.error(request, 'Failed to authenticate user.')
                    return redirect("login:register")
        else:
            messages.info(request,'password not matching')
            return redirect("login:register")

    else:
        return render(request,"registration.html")

def logout(request):
    auth.logout(request)
    #return redirect(reverse('login:login'))
    return redirect(settings.LOGOUT_REDIRECT_URL)

@login_required
def userprofile(request):
    return render(request,'user.html')

def update(request):
    user=request.user
    form=UserForm(request.POST or None,instance=user)
    if request.method=='POST':
        password=request.POST.get('password')
        entered_password = request.POST.get('new password')
        if check_password(password, user.password):
            if form.is_valid():
                user.set_password(entered_password)
                form.save()
                update_session_auth_hash(request, user)
                return redirect('login:user')
        else:
            messages.info(request, 'password not matching')
    print(form.initial)
    return render(request,'update.html',dict(form=form))

def admin(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('Password')
        user=auth.authenticate(username=username,password=password)
        if user is not None and user.is_staff:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'invalid credntials')
            return redirect('login:admin')

    return render(request,'login.html',{'user_type':'admin'})
