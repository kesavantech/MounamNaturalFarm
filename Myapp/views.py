from django.shortcuts import render, redirect
from . models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout

# Create your views here.

def HomeView(request):
    return render(request, "home.html")

def AboutUsView(request):
    return render(request, "about.html")

def ContactView(request):
    return render(request, "contact.html")

def RegisterView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        location = request.POST.get("location")
        address = request.POST.get("address")
        profile_image = request.FILES.get("profile_image")

        #Email Validation
        if User.objects.filter(email = email).exists():
            messages.error(request, "Email Already Exist !")
            return redirect("register")
        if User.objects.filter(phone = phone).exists():
            messages.error(request, "Phone No Already Exist !")

        User.objects.create_user(
            username = username, email=email, phone=phone,
            password=password, profile_image=profile_image,location = location, 
            address = address, role=User.Role.CLIENT
        )
        messages.success(request, "Successfully Registred !")
        return redirect("login")
    return render(request, "register.html")


def LoginView(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(
                request,
                "login.html",
                {"error": "Please enter correct credentials!"}
            )

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Please enter correct credentials!"}
        )

    return render(request, "login.html")

def LogoutView(request):

    if request.method == "POST":
        logout(request)
        return redirect("home")

    return render(request, "logout.html")

def ManageBaseView(request):
    return render(request, "manage_base.html")

def DashboardView(request):
    return render(request, "dashboard.html")