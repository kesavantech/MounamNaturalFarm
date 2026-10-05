from django.shortcuts import render, redirect
from . models import User, Website, HomePage,AboutUs, Enquiry
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def HomeView(request):
    home_data = HomePage.objects.all()
    context = {"home_data":home_data}
    return render(request, "home.html", context)

def AboutUsView(request):
    aboutus = AboutUs.objects.get(id=1)
    return render(request, "about.html",
                  {"aboutus":aboutus})

def ContactUsView(request):

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Enquiry.objects.create(
            name=name,
            phone=phone,
            email=email,
            message=message
        )

        messages.success(
            request,
            "Your message has been sent successfully!"
        )

        return redirect("contact")

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

            messages.success(
                request,
                f"Welcome back, {user.username}! Login successful."
            )

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


@login_required(login_url="login")
def DashboardView(request):
    return render(request, "dashboard.html")

@login_required(login_url="login")
def UserListView(request):
    if request.user.role != "ADMIN":
        return redirect("home")
    return render(request, "users.html")

@login_required(login_url="login")
def ManageBaseView(request):
    print("Username:",request.user.username)
    if request.user.role != "ADMIN":
        return redirect("home")

    website, created = Website.objects.get_or_create(id=1)
    if request.method == "POST":
            logo = request.FILES.get("logo")
            logo_radius = request.POST.get("logo_radius")
            heading = request.POST.get("heading")
            sub_heading = request.POST.get("sub_heading")
            text_color = request.POST.get("text_color")
            bg_color = request.POST.get("bg_color")
            font_size = request.POST.get("font_size")
            description = request.POST.get("description")

            if logo:
                website.logo = logo
            website.logo_radius = logo_radius
            website.heading = heading
            website.sub_heading = sub_heading
            website.text_color = text_color
            website.bg_color = bg_color
            website.font_size = font_size
            website.description = description

            website.save()
            messages.success(request, "Website Settings Updated Successfully !")
            return redirect("manage_base")
    return render(request, "manage_base.html", 
                  {"website": website})


@login_required(login_url="login")
def EnquiryView(request):

    if request.user.role != "ADMIN":
        messages.error(request, "Access Denied!")
        return redirect("home")

    enquiries = Enquiry.objects.all().order_by("-created_at")

    return render(
        request,
        "enquiry.html",
        {"enquiries": enquiries}
    )

@login_required(login_url="login")
def ManageHomeView(request):

    if request.user.role != "ADMIN":
        messages.error(request, "Access Denied !")
        return redirect("home")

    if request.method == "POST":

        # Get all submitted values
        main_images = request.FILES.getlist("main_image")
        titles = request.POST.getlist("title")
        sub_titles = request.POST.getlist("sub_title")
        bullet_1 = request.POST.getlist("bullet_point_1")
        bullet_2 = request.POST.getlist("bullet_point_2")
        bullet_3 = request.POST.getlist("bullet_point_3")

        # Delete old Home Page data
        HomePage.objects.all().delete()

        # Create new Home Page data
        for i in range(len(titles)):

            HomePage.objects.create(
                main_image=main_images[i],
                title=titles[i],
                sub_title=sub_titles[i],
                bullet_point_1=bullet_1[i],
                bullet_point_2=bullet_2[i],
                bullet_point_3=bullet_3[i]
            )

        messages.success(
            request,
            "Home Page Updated Successfully !"
        )

        return redirect("manage_home")

    home_data = HomePage.objects.all()

    return render(
        request,
        "home_manage.html",
        {
            "home_data": home_data
        }
    )


@login_required(login_url="login")
def AboutUsManageView(request):
    if request.user.role != "ADMIN":
        messages.error(request, "Access Denied !")
        return redirect("home")

    aboutus, created = AboutUs.objects.get_or_create(id=1)
    if request.method == "POST":
        hero_image = request.FILES.get("hero_image")
        hero_title = request.POST.get("hero_title")
        hero_sub_title = request.POST.get("hero_sub_title")
        who_we_are_image = request.FILES.get("who_we_are_image")
        who_we_are_title = request.POST.get("who_we_are_title")
        who_we_are_description = request.POST.get("who_we_are_description")
        mission_title = request.POST.get("mission_title")
        mission_description = request.POST.get("mission_description")
        vision_title = request.POST.get("vision_title")
        vision_description = request.POST.get("vision_description")
        special_title = request.POST.get("special_title")
        special_description = request.POST.get("special_description")

        if hero_image:
            aboutus.hero_image = hero_image
        if who_we_are_image:
            aboutus.who_we_are_image= who_we_are_image
        aboutus.hero_title= hero_title
        aboutus.hero_sub_title = hero_sub_title

        aboutus.who_we_are_title = who_we_are_title
        aboutus.who_we_are_description = who_we_are_description

        aboutus.mission_title = mission_title
        aboutus.mission_description = mission_description

        aboutus.vision_title = vision_title
        aboutus.vision_description = vision_description

        aboutus.special_title = special_title
        aboutus.special_description = special_description

        aboutus.save()
        messages.success(request, "Successfully Updated About Us Page  !")
        return redirect("about")

    return render(request, "about_manage.html",
                  {"aboutus": aboutus})

