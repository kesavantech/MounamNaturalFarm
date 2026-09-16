from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView, name="home"),
    path("AboutUs/", views.AboutUsView, name="about"),
    path("ContactUs/", views.ContactView, name="contact"), 
    path("Register/", views.RegisterView, name="register"), 
    path("Login/", views.LoginView, name="login"), 
    path("Logout/", views.LogoutView, name="logout"), 

    path("dashboard/", views.DashboardView, name="dashboard"), 
    path("ManageBase/", views.ManageBaseView, name="manage_base"),

]