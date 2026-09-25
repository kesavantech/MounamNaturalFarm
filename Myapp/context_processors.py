from Myapp.models import Website

def WebsiteSettings(request):
    website = Website.objects.get(id=1)

    return {
        "website": website
    }
