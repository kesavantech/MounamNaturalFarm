from django.shortcuts import render, redirect
from . models import User, Website, HomePage,AboutUs, Enquiry, Activity, SocialMedia
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.

def HomeView(request):
    home_data = HomePage.objects.all()
    context = {"home_data":home_data}
    return render(request, "home.html", context)

def AboutUsView(request):
    aboutus = AboutUs.objects.get(id=1)
    return render(request, "about.html",
                  {"aboutus":aboutus})



@login_required(login_url="login")
def ManageActivityView(request):

    if request.user.role != "ADMIN":
        messages.error(request, "Access Denied!")
        return redirect("home")

    if request.method == "POST":

        activity_type = request.POST.get("activity_type")
        title = request.POST.get("title")
        sub_title = request.POST.get("sub_title")
        video = request.FILES.get("video")
        description = request.POST.get("description")
        hero_image = request.FILES.get("hero_image")

        Activity.objects.create(
            activity_type=activity_type,
            title=title,
            sub_title=sub_title,
            hero_image=hero_image,
            video = video, 
            description=description
        )

        messages.success(
            request,
            "Activity added successfully!"
        )

        return redirect("manage_activity")

    return render(request, "activity_manage.html")


def ActivityView(request, activity_type):

    activities = Activity.objects.filter(
        activity_type=activity_type
    ).order_by("-created_at")

    return render(
        request,
        "activity.html",
        {
            "activities": activities,
            "activity_type": activity_type
        }
    )

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
                {"show_register_modal": True}
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

        messages.error(
            request,
            "Please enter correct credentials!"
        )
        return redirect("login")

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
            call_no = request.POST.get("call_no")
            whatsapp_no = request.POST.get("whatsapp_no")
            email = request.POST.get("email")
            location = request.POST.get("location")

            if logo:
                website.logo = logo
            website.logo_radius = logo_radius
            website.heading = heading
            website.sub_heading = sub_heading
            website.text_color = text_color
            website.bg_color = bg_color
            website.font_size = font_size
            website.description = description
            website.call_no = call_no
            website.whatsapp_no = whatsapp_no
            website.email = email
            website.location = location

            website.save()
            messages.success(request, "Website Settings Updated Successfully !")
            return redirect("manage_base")
    return render(request, "manage_base.html", 
                  {"website": website})

def BookNoowView(request):
    return render(request, "book_now.html")

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
        messages.error(request, "Access Denied!")
        return redirect("home")

    if request.method == "POST":

        section_count = int(request.POST.get("section_count", 0))

        if section_count < 1:
            messages.error(request, "At least one Home Section is required.")
            return redirect("manage_home")

        submitted_sections = []
        submitted_ids = []
        errors = []

        existing_objects = {
            str(obj.id): obj
            for obj in HomePage.objects.all()
        }

        # Validate all submitted sections before modifying the database
        for i in range(section_count):

            section_id = request.POST.get(f"sections-{i}-id", "").strip()

            title = request.POST.get(f"sections-{i}-title", "").strip()
            sub_title = request.POST.get(f"sections-{i}-sub_title", "").strip()

            bullet_1 = request.POST.get(f"sections-{i}-bullet_point_1", "").strip()
            bullet_2 = request.POST.get(f"sections-{i}-bullet_point_2", "").strip()
            bullet_3 = request.POST.get(f"sections-{i}-bullet_point_3", "").strip()

            main_image = request.FILES.get(f"sections-{i}-main_image")

            if not all([title, sub_title, bullet_1, bullet_2, bullet_3]):
                errors.append(f"Please complete all fields in Section {i + 1}.")
                continue

            obj = None

            if section_id:

                obj = existing_objects.get(section_id)

                if not obj:
                    errors.append(f"Invalid Home Section ID in Section {i + 1}.")
                    continue

                if section_id in submitted_ids:
                    errors.append("Duplicate Home Section detected.")
                    continue

                submitted_ids.append(section_id)

                if not obj.main_image and not main_image:
                    errors.append(f"Please upload an image for Section {i + 1}.")

            else:

                if not main_image:
                    errors.append(f"Please upload an image for new Section {i + 1}.")

            submitted_sections.append({
                "object": obj,
                "main_image": main_image,
                "title": title,
                "sub_title": sub_title,
                "bullet_point_1": bullet_1,
                "bullet_point_2": bullet_2,
                "bullet_point_3": bullet_3,
            })

        if errors:
            for error in errors:
                messages.error(request, error)

            return redirect("manage_home")

        try:
            with transaction.atomic():

                # Delete only sections removed by the admin
                HomePage.objects.exclude(
                    id__in=submitted_ids
                ).filter(
                    id__in=existing_objects.keys()
                ).delete()

                # Update existing sections or create new ones
                for section in submitted_sections:

                    obj = section["object"]

                    if obj:

                        # Update existing section
                        if section["main_image"]:
                            obj.main_image = section["main_image"]

                        obj.title = section["title"]
                        obj.sub_title = section["sub_title"]
                        obj.bullet_point_1 = section["bullet_point_1"]
                        obj.bullet_point_2 = section["bullet_point_2"]
                        obj.bullet_point_3 = section["bullet_point_3"]

                        obj.save()

                    else:

                        # Create new section
                        HomePage.objects.create(
                            main_image=section["main_image"],
                            title=section["title"],
                            sub_title=section["sub_title"],
                            bullet_point_1=section["bullet_point_1"],
                            bullet_point_2=section["bullet_point_2"],
                            bullet_point_3=section["bullet_point_3"],
                        )

            messages.success(
                request,
                "Home Page Sections Updated Successfully!"
            )

        except Exception:
            messages.error(
                request,
                "Something went wrong. Your changes could not be saved."
            )

        return redirect("manage_home")

    home_data = HomePage.objects.all().order_by("id")

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

def SocialMediaView(request):

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        url = request.POST.get("url", "").strip()
        logo = request.FILES.get("logo")
        is_active = request.POST.get("is_active") == "on"


        # Save social media details
        SocialMedia.objects.create(
            name=name,
            url=url,
            logo=logo,
            is_active=is_active
        )

        messages.success(
            request,
            "Social media link added successfully!"
        )

        return redirect("social_media")

    return render(request, "social_media.html")