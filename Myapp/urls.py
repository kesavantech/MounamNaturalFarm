from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("AboutUs/", views.AboutUsView, name="about"),
    path("Activities/", views.AboutUsView, name="activiies"),
    path("ContactUs/", views.ContactUsView, name="contact"), 
    path("Register/", views.RegisterView, name="register"), 
    path("Login/", views.LoginView, name="login"), 
    path("Logout/", views.LogoutView, name="logout"), 

    path("dashboard/", views.DashboardView, name="dashboard"), 

    # Admin
    path("ManageBase/", views.ManageBaseView, name="manage_base"),
    path("UsersList/", views.UserListView, name="user_list"),
    path("Enquires/", views.EnquiryView, name="enquires"),
    path("manage_home/", views.ManageHomeView, name= "manage_home"),
    path("about_manage/", views.AboutUsManageView, name="about_us_manage"),
    path("manage-activity/",views.ManageActivityView,name="manage_activity"),
]